filePath = r'c:\Users\PC\Documents\GitHub\testing\mobile\register\index.html'

with open(filePath, 'r', encoding='utf-8') as f:
    html = f.read()

old_units = """var UNITS = [
      {key:'Beavers',   ar:'البرامعم / Beavers',   color:'#ec4899', ink:'#fff'}, // زهري
      {key:'Cubs',      ar:'الأشبال والزهرات / Cubs', color:'#facc15', ink:'#5b3a00'}, // اصفر
      {key:'Girlscouts',ar:'المرشدات / Girl Scouts',  color:'#86efac', ink:'#14532d'}, // اخضر فاتح
      {key:'Boyscouts', ar:'الكشافة / Boy Scouts',   color:'#166534', ink:'#fff'},   // اخضر غامق
      {key:'Pioneers',  ar:'المتقدم / Pioneers',  color:'#fca5a5', ink:'#7f1d1d'}, // احمر فاتح
      {key:'Rovers',    ar:'الجوالة والدليلات / Rovers', color:'#991b1b', ink:'#fff'},  // احمر غامق
      {key:'Leaders',   ar:'القادة / Leaders', color:'#4f46e5', ink:'#fff'}
    ];"""

new_units = """var UNITS = [
      {key:'Beavers',   ar:'القنادس / Beavers',   color:'#ec4899', ink:'#fff'}, // زهري
      {key:'Cubs',      ar:'الجراميز والزهرات / Cubs', color:'#facc15', ink:'#5b3a00'}, // اصفر
      {key:'Girlscouts',ar:'المرشدات / Girl Scouts',  color:'#86efac', ink:'#14532d'}, // اخضر فاتح
      {key:'Boyscouts', ar:'الكشافة / Boy Scouts',   color:'#166534', ink:'#fff'},   // اخضر غامق
      {key:'Pioneers',  ar:'الرائدات / Pioneers',  color:'#fca5a5', ink:'#7f1d1d'}, // احمر فاتح
      {key:'Rovers',    ar:'الجوالة / Rovers', color:'#991b1b', ink:'#fff'},  // احمر غامق
      {key:'Leaders',   ar:'القادة / Leaders', color:'#4f46e5', ink:'#fff'}
    ];"""

html = html.replace(old_units, new_units)

with open(filePath, 'w', encoding='utf-8') as f:
    f.write(html)

print('Successfully updated unit Arabic names!')
