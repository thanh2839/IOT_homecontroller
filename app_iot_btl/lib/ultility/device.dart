// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'package:flutter/material.dart';
import 'package:heroicons/heroicons.dart';

class Device {
  final String name;
  final String space;
  final DeviceState state;
  final BoxIcon icon;
  bool active;
  bool get isActive => active;
  set isActive(bool state) => active = state;
  Device({
    required this.name,
    required this.space,
    required this.state,
    required this.icon,
    this.active = false,
  });
}

class DeviceState {
  final String label;
  //final String value;
  final String indicator;
  final bool hasIndicator;
  DeviceState({
    required this.label,
    //required this.value,
    required this.indicator,
    required this.hasIndicator,
  });
}

final devices = [
  Device(
    name: 'Fan',
    space: 'Working space',
    state: DeviceState(
      label: 'Temperature',
      //value: '24',
      indicator: '',
      hasIndicator: true,
    ),
    icon: BoxIcon(
      material: Icons.air,
      isHero: false,
    ),
  ),
  Device(
    name: 'Light bulb',
    space: 'Working Space',
    state: DeviceState(
      label: 'Light',
      //value: 'Off',
      indicator: '0%',
      hasIndicator: false,
    ),
    icon: BoxIcon(
      isHero: true,
      hero: HeroIcons.lightBulb,
    ),
  ),
  Device(
    name: 'Door',
    space: 'Yard',
    state: DeviceState(
      label: 'Volume',
      //value: '60',
      indicator: '',
      hasIndicator: true,
    ),
    icon: BoxIcon(
      isHero: true,
      hero: HeroIcons.home,
    ),
  ),
  Device(
    name: 'Alert',
    space: '',
    state: DeviceState(
      label: 'flame',
      //value: '5',
      indicator: 'users',
      hasIndicator: false,
    ),
    icon: BoxIcon(
      material: Icons.podcasts,
      isHero: false,
    ),
  ),

];

class BoxIcon {
  final IconData? material;
  final HeroIcons? hero;
  final bool isHero;
  BoxIcon({required this.isHero, this.material, this.hero})
      : assert(
          material == null || hero == null,
          'You can only use one icon type at a time',
        );
}
