import 'package:audioplayers/audioplayers.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';

class FireController extends GetxController {
  var dataController = {};
  AudioPlayer audioPlayer = AudioPlayer();
  void playAlertSound() {
    audioPlayer = AudioPlayer();
    audioPlayer.play(AssetSource('alertsound.wav'));
  }
  void stopAlertSound() {
    audioPlayer?.stop();
  }
}
