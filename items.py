import utility
import request

async def item(ctx, item_name):
    print(item_name)
    item_data = await request.getItem(ctx, item_name.replace(" ", "-"))
    item_img = "https://www.serebii.net/itemdex/sprites/pgl/" + item_name.replace(" ", "") + ".png"
    print(item_img)
    item_desc = item_data['effect_entries'][0]['effect']
    item_url = "https://bulbapedia.bulbagarden.net/wiki/" + item_name.replace(" ", "_")

    await utility.show(item_url, item_img, ctx, title=item_name, description=item_desc)
    