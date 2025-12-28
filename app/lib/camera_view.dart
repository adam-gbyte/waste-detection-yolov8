import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'main.dart';
import 'detector.dart';
import 'preprocess.dart';
import 'postprocess.dart';
import 'detection_pointer.dart';

class CameraView extends StatefulWidget {
  const CameraView({super.key});

  @override
  State<CameraView> createState() => _CameraViewState();
}

class _CameraViewState extends State<CameraView> {
  late CameraController controller;
  final detector = Detector();
  List<Detection> detections = [];

  @override
  void initState() {
    super.initState();
    init();
  }

  Future<void> init() async {
    await detector.load(); // tunggu model siap

    controller = CameraController(
      cameras.first,
      ResolutionPreset.medium,
      enableAudio: false,
    );

    await controller.initialize();
    controller.startImageStream(onFrame);

    setState(() {});
  }

  void onFrame(CameraImage image) async {
    final rgb = convert(image);
    final input = preprocess(rgb);
    final output = detector.run(input);
    final result = decode(output, 0.3);
    setState(() => detections = result);
  }

  @override
  Widget build(BuildContext context) {
    if (!controller.value.isInitialized) {
      return const Center(child: CircularProgressIndicator());
    }

    return Stack(
      children: [
        CameraPreview(controller),
        CustomPaint(painter: DetectionPainter(detections)),
      ],
    );
  }
}
