import utility
import request

class Ability:


    def __init__(self, ctx):
        self.ctx = ctx
        self.pokeID = -1
        self.abilities = []
        self.title = "";
        self.desc = "";
        self.ability_name = ""
        self.ability = ""
        self.effect = ""


    async def possible_abilities(self):
        """[Look up all possible abilities for a pokemon]

        Args:
            ctx ([context]): [The person sending the message]
            pokeID ([Int]): [The dex number of the pokemon]

        Returns:
            [List]: [A list of the possible abilities]
        """
        pokemon = await utility.get_poke(self.ctx, self.pokeID)
        ability_list = pokemon["abilities"]

        for ability in ability_list:
            print("Ability " + str(ability))
            self.abilities.append(ability["ability"]["name"])

        self.title = pokemon["name"]
        self.desc = self.abilities


    async def ability_lookup(self, ability):
        self.ability_name = ability
        self.ability = ability.strip().replace(" ", "-")
        ability_info = await request.getAbility(self.ctx, self.ability)
        print("effect_entries " + str(ability_info))
        effect_entries = ability_info["effect_entries"]

        for entry in effect_entries:
            if (entry["language"]["name"] ==  "en"):
                self.effect = entry["effect"]
                break;
        
        self.title = self.ability_name
        self.desc = self.effect


    async def ability_show(self):
        print("ability_show")
        print(str(self.pokeID) + " Here buddy")
        ability = (self.pokeID == -1)
        url_suffx = self.title + (" (Ability)" if (ability) else " (Pokémon)")
        print("Url_suffx: " + str(url_suffx))
        img = "" if (ability) else "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/" + str(self.pokeID) + ".png"
        url = "https://bulbapedia.bulbagarden.net/wiki/" + url_suffx.title().replace(" ", "_")
        await utility.show(url, img, self.ctx, title = self.title, description=self.desc)

    
    async def is_this_ability(self, check):
        pokemon = await request.getPokemon(self.ctx, check, give_error=False)
        if (pokemon != -1):
            print("here----------------")
            self.pokeID = pokemon["id"]
            return False
        return True
            
