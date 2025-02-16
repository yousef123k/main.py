from tkinter import *
from tkinter import messagebox
from pytube import YouTube 
import fluter
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await FlutterDownloader.initialize();
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'YouTube Downloader',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: DownloadScreen(),
    );
  }
}

class DownloadScreen extends StatefulWidget {
  @override
  _DownloadScreenState createState() => _DownloadScreenState();
}

class _DownloadScreenState extends State<DownloadScreen> {
  final TextEditingController _urlController = TextEditingController();
  bool _isDownloading = false;
  String _downloadStatus = '';

  Future<void> _downloadVideo(String url, bool isAudioOnly) async {
    setState(() {
      _isDownloading = true;
      _downloadStatus = 'جارٍ التحضير...';
    });

    try {
      final yt = YoutubeExplode();
      final video = await yt.videos.get(url);

      setState(() {
        _downloadStatus = 'جارٍ التنزيل...';
      });

      final streamInfo = isAudioOnly
          ? await yt.videos.streamsClient.getAudioOnly(video.id)
          : await yt.videos.streamsClient.getMuxed(video.id);

      final stream = streamInfo.first;
      final directory = await getExternalStorageDirectory();
      final filePath = '${directory!.path}/${video.title}.${stream.container.name}';

      await FlutterDownloader.enqueue(
        url: stream.url.toString(),
        savedDir: directory.path,
        fileName: '${video.title}.${stream.container.name}',
        showNotification: true,
        openFileFromNotification: true,
      );

      setState(() {
        _isDownloading = false;
        _downloadStatus = 'تم التنزيل: ${video.title}';
      });
    } catch (e) {
      setState(() {
        _isDownloading = false;
        _downloadStatus = 'حدث خطأ: $e';
      });
    }
  }

  Future<void> _requestPermissions() async {
    await Permission.storage.request();
  }

  @override
  void initState() {
    super.initState();
    _
