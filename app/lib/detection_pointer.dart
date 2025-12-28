import 'package:flutter/material.dart';
import 'postprocess.dart';

class DetectionPainter extends CustomPainter {
  final List<Detection> detections;

  DetectionPainter(this.detections);

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = Colors.red
      ..strokeWidth = 2
      ..style = PaintingStyle.stroke;

    for (final d in detections) {
      final rect = Rect.fromLTWH(
        (d.x - d.w / 2) * size.width,
        (d.y - d.h / 2) * size.height,
        d.w * size.width,
        d.h * size.height,
      );
      canvas.drawRect(rect, paint);
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
}
