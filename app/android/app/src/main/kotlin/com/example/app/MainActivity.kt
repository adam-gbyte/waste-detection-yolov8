package com.example.app

import io.flutter.embedding.android.FlutterActivity
import android.Manifest
import android.os.Bundle
import androidx.core.app.ActivityCompat

class MainActivity: FlutterActivity() {
  override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    ActivityCompat.requestPermissions(this, arrayOf(Manifest.permission.CAMERA), 0)
  }
}
