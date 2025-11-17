import aiohttp  # A library for asynchronous HTTP requests
import random
import asyncio
from datetime import datetime, timedelta

now = datetime.now()
start_date = datetime(2024, 1, 25)
future_date = start_date + timedelta(days=7)
print("Waktu dan tanggal saat ini:", now)
print("Tanggal di 7 hari mendatang di hitung dari sekarang:", future_date)
class Pokemon:
    pokemons = {}
    # Object initialisation (constructor)
    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        self.abilities = []
        self.last_feed_time = datetime.now()
        self.hp = random.randint(100,300)
        self.sp = random.randint(15,25)
        if pokemon_trainer not in Pokemon.pokemons:
            Pokemon.pokemons[pokemon_trainer] = self
        else:
            self = Pokemon.pokemons[pokemon_trainer]

    async def get_name(self):
        # An asynchronous method to get the name of a pokémon via PokeAPI
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # URL API for the request
        async with aiohttp.ClientSession() as session:  # Opening an HTTP session
            async with session.get(url) as response:  # Sending a GET request
                if response.status == 200:
                    data = await response.json()  # Receiving and decoding JSON response
                    return data['forms'][0]['name']  # Returning a Pokémon's name
                else:
                    return "Pikachu"  # Return the default name if the request fails
                
    async def get_abilities(self):
        # An asynchronous method to retrieve the URL of a pokémon image via PokeAPI
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # URL API for the request
        async with aiohttp.ClientSession() as session:  # Opening an HTTP session
            async with session.get(url) as response:  # Sending a GET request
                if response.status == 200:
                    data = await response.json()  # Receiving and decoding JSON response
                    data_list = []
                    try:
                        for i in range(2):
                            data_list.append(data['abilities'][i]['ability']['name'])
                        return data_list  # Returning a Pokémon's name
                    except:
                        data_list.append(data['abilities'][0]['ability']['name'])
                        return data_list
                else:
                    return "Placeholder Pikachu Image"  # Return the default name if the request fails

    async def info(self):
        # A method that returns information about the pokémon
        if not self.name:
            self.name = await self.get_name()  # Retrieving a name if it has not yet been uploaded
            self.abilities = await self.get_abilities()
            if len(self.abilities) > 1:
                return f"The name of your Pokémon: {self.name} \n Abilities: {self.abilities[0]} and {self.abilities[1]}\n Health: {self.hp} \n Stamina: {self.sp}" 
            else:
                return f"The name of your Pokémon: {self.name} \n Abilities: {self.abilities[0]}\n Health: {self.hp} \n Stamina: {self.sp}"   # Returning the string with the Pokémon's name

    async def show_img(self):
        # An asynchronous method to retrieve the URL of a pokémon image via PokeAPI
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # URL API for the request
        async with aiohttp.ClientSession() as session:  # Opening an HTTP session
            async with session.get(url) as response:  # Sending a GET request
                if response.status == 200:
                    data = await response.json()  # Receiving and decoding JSON response
                    return data['sprites']['other']['home']['front_default']  # Returning a Pokémon's name
                else:
                    return "Placeholder Pikachu Image"  # Return the default name if the request fails
                
    async def attack(self, enemy):
        if isinstance(enemy, Wizard):  # Periksa apakah musuh adalah tipe data Penyihir (instance dari kelas Penyihir)
            kesempatan = random.randint(1,5)
            if kesempatan == 1:
                return "Pokemon penyihir menggunakan perisai dalam pertarungan"
        if enemy.hp > self.sp:
            enemy.hp -= self.sp
            return f"Pertarungan @{self.pokemon_trainer} dengan @{enemy.pokemon_trainer}"
        else:
            enemy.hp = 0
            return f"@{self.pokemon_trainer} menang melawan @{enemy.pokemon_trainer}!"
        
    async def feed(self, feed_interval = 20, hp_increase = 10 ):
        current_time = datetime.current()  
        delta_time = timedelta(hours=feed_interval)  
        if (current_time - self.last_feed_time) > delta_time:
            self.hp += hp_increase
            self.last_feed_time = current_time
            return f"Kesehatan Pokemon dipulihkan. HP saat ini: {self.hp}"
        else:
            return f"Kalian dapat memberi makan Pokémon kalian di: {current_time-delta_time}"
        

class Fighter(Pokemon):
    async def attack(self, enemy):
        kekuatan_super = random.randint(5,15)
        self.sp += kekuatan_super
        hasil = await super().attack(enemy)
        self.sp -= kekuatan_super
        return hasil + f"\nPetarung menggunakan serangan super dengan kekuatan:{kekuatan_super} "

    async def feed(self, feed_interval = 25, hp_increase = 20 ):
        current_time = datetime.current()  
        delta_time = timedelta(hours=feed_interval)  
        if (current_time - self.last_feed_time) > delta_time:
            self.hp += hp_increase
            self.last_feed_time = current_time
            return f"Kesehatan Pokemon dipulihkan. HP saat ini: {self.hp}"
        else:
            return f"Kalian dapat memberi makan Pokémon kalian di: {current_time-delta_time}"

class Wizard(Pokemon):
    async def attack(self, enemy):
        return await super().attack(enemy)
    
    async def feed(self, feed_interval = 10, hp_increase = 8 ):
        current_time = datetime.current()  
        delta_time = timedelta(hours=feed_interval)  
        if (current_time - self.last_feed_time) > delta_time:
            self.hp += hp_increase
            self.last_feed_time = current_time
            return f"Kesehatan Pokemon dipulihkan. HP saat ini: {self.hp}"
        else:
            return f"Kalian dapat memberi makan Pokémon kalian di: {current_time-delta_time}"
    
async def main():
    wizard = Wizard("username1")
    fighter = Fighter("username2")

    print(await wizard.info())
    print()
    print(await fighter.info())
    print()
    print(await fighter.attack(wizard))

if __name__ == '__main__':
    asyncio.run(main())