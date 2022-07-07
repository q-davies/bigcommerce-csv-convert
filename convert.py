from pathlib import Path
import csv

def convert_line(f, source_fields):

    # source_fields = source_line.split(',')

    product_id = source_fields[0]

    if product_id == "":
        item_type = "SKU"
        option1_name = source_fields[8]
        option1_value = source_fields[9]
        option2_name = source_fields[10]
        option2_value = source_fields[11]
        product_name = f"[RT]{option1_name}={option1_value}"
        if option2_name != "":
            product_name = product_name + f",[RT]{option2_name}={option2_value}"
    else:
        item_type = "PRODUCT"
        product_name = source_fields[5]

    product_type = 'P'
    sku = source_fields[7]
    option_set = ''
    option_set_align = ''
    product_description = source_fields[6].replace("\"", "'")
    price = source_fields[20]
    sale_price = source_fields[21]
    weight = source_fields[26]
    height = source_fields[29]
    depth = source_fields[27]
    width = source_fields[28]
    allow_purchases = ''
    is_visible = source_fields[30]
    availability = ''
    if item_type == "PRODUCT":
        track_inventory = "by product"
    else:
        track_inventory = ''
    current_stock = source_fields[23]
    category = source_fields[24].replace(",", ";").replace("/", "", 1).replace("; /", ";").replace(";/", ";")
    product_image_id = ''
    product_image_url = source_fields[31]
    product_image_description = ''
    product_image_is_thumbnail = ''
    product_image_sort = ''
    search_keywords = source_fields[25]
    page_title = ''
    product_url = ''

    target_line = f"\"{item_type}\",\"{product_id}\",\"{product_name}\",\"{product_type}\",\"{sku}\",,,\"{option_set}\",\"{option_set_align}\",\"{product_description}\",\"{price}\",,,\"{sale_price}\",,,,\"{weight}\",\"{width}\",\"{height}\",\"{depth}\",\"{allow_purchases}\",\"{is_visible}\",\"{availability}\",\"{track_inventory}\",\"{current_stock}\",,\"{category}\",\"{product_image_id}\",\"{product_image_url}\",\"{product_image_description}\",\"{product_image_is_thumbnail}\",\"{product_image_sort}\",,,,,,\"{search_keywords}\",\"{page_title}\",,,,,,,,,,,,,,,,,\"{product_url}\",,,,,,,,,,,,\n"
 
    f.write(target_line)
    f.flush()

    return

def create_file(file_name, header):
    p = Path(file_name)

    f = p.open('w')

    f.write(header)

    return f

def read_file(file_name):
    # p = Path(file_name)

    # f = p.open('r', encoding='utf-8')
    lines = []
    with open(file_name, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            # print(','.join(row))
            lines.append(row)

    return lines

# open template
template_lines = read_file('bulk-edit-product-import-template.csv')

# open source file
# manual edits to the downloaded file from square space
# Remove extra https at end of image url
# Replace hard-coded word bullet character with <li>
# Replace \n with <br/>
# Replace ″ with &rdquo;
source_lines = read_file('products_squarespace_cottoncuts.csv')
print(source_lines[4])

header = ','.join(template_lines[0])

out_file = create_file('bulk-edit-product-import-cottoncuts.csv', header)

# for each line in source, convert
for source_line in source_lines:
    convert_line(out_file, source_line)