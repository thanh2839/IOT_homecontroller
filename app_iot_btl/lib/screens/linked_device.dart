import 'package:firebase_database/firebase_database.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:app_iot_btl/ultility/context.dart';
import 'package:app_iot_btl/ultility/device.dart';
import 'package:go_router/go_router.dart';
import 'package:heroicons/heroicons.dart';
import 'package:redacted/redacted.dart';

class _SwitchNotifier extends ValueNotifier<bool> {
  var index;

  _SwitchNotifier(bool value, this.index) : super(value);

  void toggle() => value = !value;
}

class DeviceBox extends StatelessWidget {
  DeviceBox({
    required this.device,
    super.key,
  });
  final Device device;
  final database = FirebaseDatabase.instance.ref('btl-iot');
  @override
  Widget build(BuildContext context) {
    final switchNotifier = _SwitchNotifier(device.isActive, device.name);
    return GestureDetector(
      onTap: () => context.pushNamed('air-conditionner'),
      child: ValueListenableBuilder(
        valueListenable: switchNotifier,
        builder: (context, active, _) {
          return AnimatedContainer(
            duration: const Duration(milliseconds: 400),
            //  curve: Curves.easeInOut,
            height: 200,
            decoration: BoxDecoration(
              color: !active ? context.boxColor : null,
              gradient: active
                  ? LinearGradient(
                begin: Alignment.topCenter,
                end: Alignment.bottomCenter,
                colors: [
                  context.colorScheme.primary,
                  context.colorScheme.secondary,
                ],
              )
                  : null,
              borderRadius: BorderRadius.circular(24),
            ),
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // 2.vGap,
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Container(
                        width: 45,
                        height: 45,
                        decoration: BoxDecoration(
                          color: active
                              ? context.colorScheme.onBackground
                              : context.colorScheme.background,
                          shape: BoxShape.circle,
                        ),
                        child: Padding(
                          padding: const EdgeInsets.all(4),
                          child: Center(
                            child: Visibility(
                              visible: device.icon.isHero,
                              replacement: Icon(
                                device.icon.material,
                                size: 28,
                                color: !active
                                    ? context.colorScheme.onBackground
                                    : context.colorScheme.background,
                              ),
                              child: HeroIcon(
                                device.icon.isHero
                                    ? device.icon.hero!
                                    : HeroIcons.variable,
                                size: 28,
                                color: !active
                                    ? context.colorScheme.onBackground
                                    : context.colorScheme.background,
                              ),
                            ),
                          ),
                        ),
                      ),
                      Column(
                        children: [
                          Row(
                            children: [
                              /*Text(
                                device.state.value,
                                style: context.textTheme.bodyLarge!.copyWith(
                                  fontSize: 24,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),*/
                              if (device.state.hasIndicator)
                                Transform.translate(
                                  offset: const Offset(0, -7.5),
                                  child: Text(
                                    device.state.indicator,
                                    style:
                                    context.textTheme.bodyLarge!.copyWith(
                                      fontSize: 14,
                                      fontWeight: FontWeight.bold,
                                    ),
                                  ),
                                ),
                            ],
                          ),
                          if (!device.state.hasIndicator)
                            Text(
                              device.state.label,
                              style: context.textTheme.bodyLarge!.copyWith(
                                fontSize: 11,
                                color: context.subtitleColor,
                              ),
                            ),
                        ],
                      ),
                    ],
                  ),
                  const Spacer(),
                  Text(
                    device.space,
                    style: context.textTheme.bodyLarge!.copyWith(
                      fontSize: 10,
                      color: context.subtitleColor,
                    ),
                  ),
                  Text(
                    device.name,
                    style: context.textTheme.bodyLarge!.copyWith(
                      fontSize: 15,
                      fontWeight: FontWeight.bold,
                      color: active
                          ? context.colorScheme.background
                          : context.colorScheme.onBackground,
                    ),
                  ),
                  Switch.adaptive(
                    value: active,
                    applyCupertinoTheme: true,
                    activeColor: context.colorScheme.onBackground,
                    activeTrackColor: context.colorScheme.background,
                    inactiveTrackColor: Colors.transparent,
                    inactiveThumbColor: context.colorScheme.onBackground,
                    onChanged: (state) =>
                    {
                      switchNotifier.value = state,
                      if(switchNotifier.index == 'Fan'){
                        database.update({
                          "fan": state,
                        })
                      }
                      else
                        if (switchNotifier.index == 'Light bulb'){
                          database.update({
                            "light": state
                          })
                        }
                        else
                          if (switchNotifier.index == 'Alert'){
                            database.update({
                              "flame": state ? 0 : 1
                            })
                          }
                          else
                            if (switchNotifier.index == 'Door'){
                              database.update({
                                "face-detect": state
                              })
                            }
                    }
                  ),
                ],
              ),
            ),
          ).redacted(context: context, redact: false);
        },
      ),
    );
  }
}