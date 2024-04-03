<H1>R+MotionDataConverter</H1>
<H5>Mengambil data bucket, movie dan unit dari file .mtnx dari R+Motion ke file .json</H5>

lokasi python script */src/script/converter.py<br>
c++ parser */src/main.cpp (durung) <br>

<h3>Panduan Script Python</h3>

<img>![nama file](https://github.com/rahmadupi/R-MotionDataConverter/assets/49749488/af5ded4d-d262-465c-a4d6-8baccf7eab03)</img>
<p>- Masukan lokasi dari file .mtnx pada variable yang sesuai<br><i>Note: Pastikan terdapat penanda tipe servo "MX" atau "XL" dalam nama file .mtnx</i></p>

<img>![lokasi untuk output](https://github.com/rahmadupi/R-MotionDataConverter/assets/49749488/b5072e24-10d8-47d9-bfe7-3d14a1fcef5b)</img>
<p>- Spesifikasikan dimana file json akan ditaruh, secara default file json akan disimpan kedalam folder data dan difolder dengan nama tipe servo yang sesuai<br>- Output berupa 2 file json untuk motion bucket dan motion movie dan 1 folder berisi setiap motion unit dalam file json secara terpisah</p>
<br>

![image](https://github.com/rahmadupi/R-MotionDataConverter/assets/49749488/99356b10-7850-4a3f-83d3-302dfe2a6da0)

<h3>Struktur Dalam File Json</h3>
<p>Motion Bucket dan Movie terpisah dalam 2 file dan untuk motion unit terpisah dalam satu folder sendiri dimana setiap file dalam folder motion unit berisi 1 motion unit</p>

  <h5>- Bucket</h5> 

  https://github.com/rahmadupi/R-MotionDataConverter/blob/a703f876d18b52e1a2dc9b862c1e97a3d4547eb2/data/MX/motion_bucket.json#L1-L38

  
  
  <p>- Dalam file motion bucket terdapat key BUCKET berisi list dari seluruh data bucket<br>  dalam data bucket berisi id, nama, total motion movie dalam bucket dan terakhir key motion movie yang berisi list dari id motion movie yang ada dalam bucket</p>

  <h5>- Movie</h5>
  
  https://github.com/rahmadupi/R-MotionDataConverter/blob/a703f876d18b52e1a2dc9b862c1e97a3d4547eb2/data/MX/motion_movie.json#L1-L522
  <p>- Struktur dalam motion movie sama seperti motion bucket dengan, key MOVIE sebagai root dan berisi list dari motion movie itu sendiri, setiap motion movie berisi id, nama dan total unit dari unit yang berada dalam motion movie tersebut.<br>dalam list motion unit tersebut setiap item menyimpan data id, speed dan loop motion unit</p>

  <h5>- Unit</h5>
  https://github.com/rahmadupi/R-MotionDataConverter/blob/a703f876d18b52e1a2dc9b862c1e97a3d4547eb2/data/MX/motion_unit/1.json#L1
  <p>- Untuk motion unit dipisah setiap file karena banyaknya data, sehingga setiap file berisi satu motion unit dan dalam motion unit tercantum data id, nama, total frame, list waktu transisi untuk setiap frame dan list isi dari motion frame itu sendiri. dalam motion frame berisi data posisi untuk 16 servo</p>






