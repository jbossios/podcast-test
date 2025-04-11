import yaml
import xml.etree.ElementTree as xml_tree


if __name__ == '__main__':

    with open('feed.yaml', 'r') as file:
        yaml_data = yaml.safe_load(file)

    rss_element = xml_tree.Element('rss', {
        'version': '2.0',
        'xmlns:itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd',
        'xmlns:content': 'http://purl.org/rss/1.0/modules/content/'
    })

    channel_element = xml_tree.SubElement(rss_element, 'channel')

    link_prefix = yaml_data['link']

    options_xml = {
        'title': 'title',
        'format': 'format',
        'subtitle': 'subtitle',
        'author': 'itunes:author',
        'description': 'description',
        'image': 'itunes.image',
        'language': 'language',
    }

    for option in options_xml:
        option_xml = options_xml[option]
        if option != 'image':
            xml_tree.SubElement(channel_element, option_xml).text = yaml_data[option]
        else:
            xml_tree.SubElement(channel_element, option_xml, {'href': link_prefix + yaml_data[option]})

    xml_tree.SubElement(channel_element, 'link').text = link_prefix

    xml_tree.SubElement(channel_element, 'itunes:category', {'text': yaml_data['category']})

    for item in yaml_data['item']:
        item_element = xml_tree.SubElement(channel_element, 'item')
        xml_tree.SubElement(item_element, 'title').text = item['title']
        xml_tree.SubElement(item_element, 'description').text = item['description']
        xml_tree.SubElement(item_element, 'pubDate').text = item['published']
        xml_tree.SubElement(item_element, 'itunes:author').text = yaml_data['author']
        xml_tree.SubElement(item_element, 'itunes:duration').text = item['duration']

        enclosure = xml_tree.SubElement(item_element, 'enclosure', {
            'url': link_prefix + item['file'],
            'type': 'audio/mpeg',
            'length': item['length']
        })

    output_tree = xml_tree.ElementTree(rss_element)
    output_tree.write('podcast.xml', encoding='UTF-8', xml_declaration=True)