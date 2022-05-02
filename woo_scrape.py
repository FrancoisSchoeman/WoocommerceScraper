from requests_html import HTMLSession
import csv
import time

# CATEGORY = 'single category'

def main(category):
    s = HTMLSession()
    
    # TODO CHANGE URL
    url = f'https://www.liteglo.co.za/product-category/{category}/?product_count=144'

    def get_links(url):  # sourcery skip: inline-immediately-returned-variable
        r = s.get(url)
        # Selector for an individual product item
        items = r.html.find('div.fusion-product-wrapper')

        # Return Links
        return [links.append(item.find('a', first=True).attrs['href']) for item in items]

    def get_productdata(link):
        r = s.get(link)
        title = r.html.find('h1', first=True).full_text
        price = r.html.find('span.woocommerce-Price-amount.amount bdi')[0].full_text

        # Get description from product page
        description = r.html.find('div.fusion-content-tb ul')[0].text
        image = r.html.find('img.wp-post-image')[0].attrs['data-srcset']
        image = image.split(',')[-1][:-5]
        # tag = r.html.find('a[rel=tag]', first=True).full_text
        # sku = r.html.find('span.sku', first=True).full_text
        
        product = {
            'title': title.strip(),
            'price': price.strip(),
            'image': image.strip(),
            'description': description,
            # 'tag': tag.strip(),
            # 'sku': sku.strip()
        }
        print(product)
        return product

    results = []
    links = get_links(url)

    for link in links:
        results.append(get_productdata(link))
        time.sleep(1)

    with open(f'{category}.csv', 'w', encoding='utf8', newline='') as f:
        fc = csv.DictWriter(f, fieldnames=results[0].keys())
        fc.writeheader()
        fc.writerows(results)
        print(f'\n{category} done\n')


if __name__ == '__main__':
    # TODO ENTER CATEGORIES HERE
    category_list = ['list', 'of', 'categories']

    for category in category_list:
        main(category)