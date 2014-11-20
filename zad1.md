# Zadanie 1

## a)
Wstepne przygotowanie danych przy uzyciu skryptu bash 2unix.sh. Import danych do kolekcji 'train' w bazie 'zadanie'.
```
time ./mongoimport.exe -d zadanie -c train --type csv --file d:/nosql/data.csv --headerline
```

Czas wykonania:

```
real    9m15.527s
user    0m0.000s
sys     0m0.015s
```

## b)

```
db.train.count()
6034195
```

## c)
Skrypt zamieniajacy stringa z tagami (ze spacja jako separatorem) na tablice stringow:
```
var db = new Mongo().getDB('zadanie');
var records = db.train.find();

records.forEach(function(element) {
  if(typeof(element.tags) === 'string') {
    var newTags = element.tags.split(' ');

    db.train.update(
      {_id: element._id},
      {$set: {tags: newTags}}
    )
  }
});
```
Czas wykonania operacji:
```
real    34m20.849s
user    0m0.000s
sys     0m0.015s
```
---
Ilosc tagow
```
var db = new Mongo().getDB('zadanie');
var records = db.train.find();

var count = 0;

records.forEach(function(element) {
  if(element.tags instanceof Array) {
    count += element.tags.length;
  }
});

print('Ilosc tagow: ' + count);
```
Wynik:
```
17408733

real    4m18.352s
user    0m0.000s
sys     0m0.015s
```

Ilosc unikalnych tagow
```
var db = new Mongo().getDB('zadanie');
var records = db.train.find();

var oTags = {};

records.forEach(function(element) {
  if(element.tags instanceof Array) {
    for(i = 0; i < element.tags.length; i++) {
      var name = element.tags[i];
      if(typeof oTags[name] === 'undefined') {
        oTags[name] = 1;
      }
      else {
        oTags[name] += 1;
      }
    }
  }
});

print(Object.keys(oTags).length);
```
Wynik:
```
42048

real    4m16.065s
user    0m0.000s
sys     0m0.000s
```

## d)

Import pliku JSON zawierajacego polozenia miast wojewodzkich w Polsce:
```
$ time ./mongoimport.exe -c places --file D:/nosql/miasta.json --type json
connected to: 127.0.0.1
2014-11-19T22:54:46.166+0000 check 9 17
2014-11-19T22:54:46.166+0000 imported 17 objects

real    0m1.198s
user    0m0.000s
sys     0m0.015s
```

Dodanie indeksu:
```
db.places.ensureIndex({"loc" : "2dsphere"})
```

### Zapytanie 1:
Miasto wojewodzkie polozone najblizej Warszawy:
```
var Warszawa = db.places.findOne({ _id: "Warszawa" })
db.places.find({loc: {$near: {$geometry: Warszawa.loc, $maxDistance: 600000}}}).skip(1).limit(1)
```
[Wynik](https://github.com/lekiert/nosql/blob/master/zapytania/z1.json)

### Zapytanie 2:
Miasta wojewodzkie znajdujace sie w promieniu 2 stopni (ok. 222.4 km) od Lodzi:
```
var Lodz = db.places.findOne({ _id: "Lodz" })
db.places.find({loc: {$geoWithin: {$center: [Lodz.loc.coordinates, 2]}}})
```
[Wynik](https://github.com/lekiert/nosql/blob/master/zapytania/z2.json)

### Zapytanie 3:
Miasta znajdujące się w czworokącie o wierzchołkach polozonych w najdalej wysunietych punktach Polski (S, E, N, W)
```
db.places.find({loc: {$geoWithin: {$geometry: polygon}}})
```
[Wynik](https://github.com/lekiert/nosql/blob/master/zapytania/z3.json)

### Zapytanie 4:
Miasta lezace na tym samym rownolezniku, co Gdansk:
```
db.places.find({loc: {$geoIntersects: {$geometry: {type: "LineString", coordinates: [[180,Gdansk.loc.coordinates[1]],[-180,Gdansk.loc.coordinates[1]]]}}}})
```
[Wynik](https://github.com/lekiert/nosql/blob/master/zapytania/z4.json)

### Zapytanie 5:
Miasta lezace na linii Gdansk-Opole:
```
var Gdansk = db.places.findOne({ _id: "Gdansk" })
var Opole = db.places.findOne({ _id: "Opole" })
db.places.find({loc: {$geoIntersects: {$geometry: {"type": "LineString", "coordinates": [Gdansk.loc.coordinates,Opole.loc.coordinates]}}}})
```
[Wynik](https://github.com/lekiert/nosql/blob/master/zapytania/z5.json)

### Zapytanie 6:
Miasta znajdujace sie w tzw. Polsce "B":
```
var polygon = {
  "type": "Polygon",
  "coordinates": [[
  [18.94043,54.342749],
  [18.71109,53.448551],
  [18.141174,53.103404],
  [19.109344,52.659466],
  [19.451294,51.821137],
  [19.264526,50.742321],
  [18.660278,49.765965],
  [22.873535,48.860198],
  [24.510498,51.066859],
  [23.708496,54.235538],
  [21.154175,54.500951],
  [18.94043,54.342749]
  ]]
}
db.places.find({loc: {$geoWithin: {$geometry: polygon}}})
```
[Wynik](https://github.com/lekiert/nosql/blob/master/zapytania/z6.json)
