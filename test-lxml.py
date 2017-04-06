# -*- coding: utf-8 -*-
from lxml import etree

xml = u"""<ymaps:ymaps xmlns:ymaps="http://maps.yandex.ru/ymaps/1.x"
        xmlns:repr="http://maps.yandex.ru/representation/1.x"
       xmlns:gml="http://www.opengis.net/gml"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://maps.yandex.ru/schemas/ymaps/1.x/ymaps.xsd"> 
    <repr:Representation> 
        <repr:Style gml:id="styleBusStop"> 
          <repr:parentStyle>default#busIcon</repr:parentStyle> 
        </repr:Style> 
    </repr:Representation>  
    <ymaps:GeoObjectCollection> 
        <gml:featureMember> 
            <ymaps:GeoObject> 
                <ymaps:style>#styleBusStop</ymaps:style> 
                <gml:name>Остановка: «М. „Бронная” ул.»</gml:name> 
                <gml:description>Автобусы: 1 2 34 121</gml:description> 
                <gml:Point> 
                    <gml:pos>37.561598 55.692394</gml:pos> 
                </gml:Point> 
            </ymaps:GeoObject> 
        </gml:featureMember> 
    </ymaps:GeoObjectCollection> 
</ymaps:ymaps>"""

#root = etree.fromstring(xml, base_url="http://tzhe.narod.ru/test.xml")
#etree.SubElement(root[0], "{http://maps.yandex.ru/representation/1.x}Style")
#root[0][1].set("{http://www.opengis.net/gml}id", "myStyle")
#etree.SubElement(root[0][1], "{http://maps.yandex.ru/representation/1.x}parentStyle")
#root[0][1][0].text = u"привет"
root = etree.fromstring(xml)
root[1][0][0][3][0].text = "71.41805827617648 51.1158373002793"
print etree.tostring(root, pretty_print=True)