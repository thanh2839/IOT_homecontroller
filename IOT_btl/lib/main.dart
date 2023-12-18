import 'dart:math';
import 'dart:ui';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_database/firebase_database.dart';
import 'package:flutter/material.dart';
import 'package:iot_btl/firebase_options.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.lightBlue),
        useMaterial3: true,
      ),
      home: const MyHomePage(title: 'Home Controller'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({Key? key, required this.title});
  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  //aaaaaaaaa
  //FirebaseDatabase database = FirebaseDatabase.instance;
  //DatabaseReference ref = FirebaseDatabase.instance.ref();
  DatabaseReference dataR = FirebaseDatabase.instance.ref('/test');

  //final dataR = FirebaseDatabase.instance.ref('DATABASE_NAME .asia-southeast1.firebasedatabase.app');
  bool On = false;
  bool lightbulb = false;
  bool fan = false;
  String temp = '0';
  String hum = '0';
  double lumen = 0;
  bool tem = false;
  bool humn = false;

  var currentDate = 'Loading...';
  //-----------------------------------
  @override
  Widget build(BuildContext context) {
    Size size = MediaQuery.of(context).size;
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Text(widget.title),
      ),
      body: Container(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text("Việt Nam",
                style: TextStyle(
                  fontWeight: FontWeight.bold,
                  fontSize: 30.0,
                )),
            Text(
              currentDate,
              style: TextStyle(color: Colors.grey, fontSize: 16.0),
            ),
            const SizedBox(
              height: 50,
            ),
            Container(
              width: size.width,
              height: 200,
              decoration: BoxDecoration(
                  color: Colors.cyan,
                  borderRadius: BorderRadius.circular(15),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.yellow.withOpacity(.5),
                      offset: const Offset(0, 25),
                      blurRadius: 10,
                      spreadRadius: -12,
                    )
                  ]),
              child: Stack(
                clipBehavior: Clip.none,
                children: [
                  Positioned(
                    top: 30,
                    left: 30,
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Padding(
                          padding: const EdgeInsets.only(top: 4.0),
                          child: Text(
                            "Nhiệt độ",
                            style: TextStyle(fontSize: 25),
                          ),
                        )
                      ],
                    ),
                  ),
                  Positioned(
                      top: 50,
                      left: 50,
                      child: Row(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Padding(
                            padding: const EdgeInsets.only(top: 4.0),
                            child: Text(
                              temp,
                              style: TextStyle(
                                fontSize: 80,
                                fontWeight: FontWeight.bold,
                                //foreground: Paint()..shader = Color
                              ),
                            ),
                          ),
                        ],
                      )),
                  Positioned(
                    top: 30,
                    right: 30,
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Padding(
                          padding: const EdgeInsets.only(top: 4.0),
                          child: Text(
                            "Độ ẩm",
                            style: TextStyle(fontSize: 25),
                          ),
                        )
                      ],
                    ),
                  ),
                  Positioned(
                      top: 50,
                      right: 50,
                      child: Row(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Padding(
                            padding: const EdgeInsets.only(top: 4.0),
                            child: Text(
                              hum,
                              style: TextStyle(
                                fontSize: 80,
                                fontWeight: FontWeight.bold,
                                //foreground: Paint()..shader = Color
                              ),
                            ),
                          ),
                        ],
                      ))
                ],
              ),
            ),
            const SizedBox(
              height: 50,
            ),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 40),
              child: Column(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Row(
                      children: [
                        Container(
                          padding: const EdgeInsets.all(10.0),
                          height: 50,
                          width: 50,
                          decoration: const BoxDecoration(
                              color: Color(0xffE0E8FB),
                              borderRadius:
                              BorderRadius.all(Radius.circular(15))),
                          child: Icon(
                            Icons.lightbulb_outline,
                            color: Colors.amber,
                          ),
                        ),
                        const Text(
                          '  Đèn',
                          style: TextStyle(color: Colors.black54, fontSize: 20),
                        ),
                        Spacer(),
                        Switch(
                          value: lightbulb,
                          activeColor: Colors.green,
                          onChanged: (value) {
                            setState(() {
                              dataR.update({"Light": value});
                              lightbulb = value;
                            });
                          },
                        ),
                        const SizedBox(
                          height: 8,
                        ),
                      ],
                    ),
                    const SizedBox(
                      height: 8,
                    ),
                    Row(
                      children: [
                        Container(
                          padding: const EdgeInsets.all(10.0),
                          height: 50,
                          width: 50,
                          decoration: const BoxDecoration(
                              color: Color(0xffE0E8FB),
                              borderRadius:
                              BorderRadius.all(Radius.circular(15))),
                          child: Icon(
                            Icons.air,
                            color: Colors.amber,
                          ),
                        ),
                        const Text(
                          '  Quạt',
                          style: TextStyle(color: Colors.black54, fontSize: 20),
                        ),
                        Spacer(),
                        Switch(
                          value: fan,
                          activeColor: Colors.green,
                          onChanged: (value) {
                            setState(() {
                              dataR.update({
                                "fan": value,
                              });
                              fan = value;
                            });
                          },
                        ),
                        const SizedBox(
                          height: 8,
                        ),
                        Spacer(),
                        Switch(
                            value: tem,
                            activeColor: Colors.green,
                            onChanged: (value) {
                              if (value == true) {
                                setState(() {
                                  //-----------------
                                  dataR.update({
                                    "humidity": Random().nextInt(100),
                                  });
                                  /*DatabaseReference datacrawlH =
                                  FirebaseDatabase.instance.ref('/btl-iot/humidity');
                              datacrawlH.onChildChanged.listen((DatabaseEvent event) {
                                var dataHum = event.snapshot.value.toString();
                                var datam = event.snapshot.value;
                                hum = dataHum;
                                print(datam);
                              });*/
                                  dataR.update({
                                    "tempurater": Random().nextInt(100),
                                  });
                                  DatabaseReference datacrawl =
                                  FirebaseDatabase.instance.ref(
                                      '/test/tempurater');
                                  datacrawl.onChildChanged.listen((
                                      DatabaseEvent event) {
                                    var data = event.snapshot.value.toString();
                                    temp = data;
                                  });
                                  humn = value;
                                  tem = value;
                                });
                              }
                            }
                        ),
                        const SizedBox(
                          height: 8,
                        ),
                      ],
                    )
                  ]),
            )
          ],
        ),
      ),
    );
  }
}
