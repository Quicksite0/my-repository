import random
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

class HuntTheWumpus:

    def __init__(self, initial_arrows=5):
        self.num_caves = 20
        self.cave_map = self._generate_cave_map()
        self.wumpus_location = -1
        self.pit_locations = []
        self.bat_locations = []
        self.player_location = -1
        self.num_arrows = initial_arrows
        self.game_over = False
        self.message = ""

        # initialize game elements
        self._place_game_elements()

    def _generate_cave_map(self):
        cave_map = {}
        rows, cols = 4, 5
        for i in range(1, self.num_caves + 1):
            connections = []
            
            # grid position calculations
            row = (i - 1) // cols
            col = (i - 1) % cols
            
            # neighbours based on grid position
            if row > 0:
                connections.append(i - cols)
            if row < rows - 1:
                connections.append(i + cols)
            if col > 0:
                connections.append(i - 1)
            if col < cols - 1:
                connections.append(i + 1)
                
            cave_map[i] = connections
        
        return cave_map

    def _place_game_elements(self):
        all_locations = list(range(1, self.num_caves + 1))
        random.shuffle(all_locations)
        self.wumpus_location = all_locations.pop()
        
        for _ in range(2):
            self.pit_locations.append(all_locations.pop())
            
        for _ in range(2):
            self.bat_locations.append(all_locations.pop())
            
        self.player_location = all_locations.pop()

    def _get_neighbors(self, cave):
        return self.cave_map.get(cave, [])

    def _get_perceptions(self):
        perceptions = []
        neighbors = self._get_neighbors(self.player_location)

        for neighbor in neighbors:
            if neighbor == self.wumpus_location:
                perceptions.append("I smell a Wumpus!")
            if neighbor in self.pit_locations:
                perceptions.append("I feel a breeze.")
            if neighbor in self.bat_locations:
                perceptions.append("I hear bats.")
        return perceptions

    def _check_hazards(self, has_planks, has_heavy_shoes):
        if self.player_location == self.wumpus_location:
            self.message = "The Wumpus got you! Game Over."
            self.game_over = True
            return True
        elif self.player_location in self.pit_locations:
            if has_planks:
                self.message = "You fell into a pit but used your wooden planks to escape!"
                return "planks"
            else:
                self.message = "You fell into a bottomless pit! Game Over."
                self.game_over = True
                return True
        elif self.player_location in self.bat_locations:
            if has_heavy_shoes:
                # Heavy shoes nullify the effect of bats
                self.message = "Giant bats swoop down, but your heavy shoes keep you firmly on the ground."
                return "heavy_shoes"
            else:
                self.message = "Giant bats snatch you and drop you in a random cave!"
                possible_locations = set(range(1, self.num_caves + 1))
                possible_locations.difference_update(
                    [self.wumpus_location] + self.pit_locations + self.bat_locations
                )
                possible_locations.discard(self.player_location)
                if possible_locations:
                    self.player_location = random.choice(list(possible_locations))
                else:
                    self.player_location = random.choice(
                        [c for c in range(1, self.num_caves + 1) if c != self.player_location]
                    )
                return False
        return False

    def move_player(self, destination, has_planks, has_heavy_shoes):
        if self.game_over:
            self.message = "The game is over. Start a new game."
            return

        if destination not in self._get_neighbors(self.player_location):
            self.message = "That's not a connected cave! Try again."
            return False

        self.player_location = destination
        self.message = f"You are now in cave {self.player_location}."
        return self._check_hazards(has_planks, has_heavy_shoes)
        
    def shoot_arrow(self, target_path):
        if self.game_over:
            self.message = "The game is over. Start a new game."
            return

        if self.num_arrows <= 0:
            self.message = "You are out of arrows! Game Over."
            self.game_over = True
            return

        self.num_arrows -= 1

        if not target_path or not isinstance(target_path, list):
            self.message = "Invalid arrow path. Please provide a list of cave numbers."
            return

        current_arrow_location = self.player_location
        valid_shot = True

        for i, target_cave in enumerate(target_path):
            if i >= 5:
                self.message = "Arrow ran out of range!"
                break

            if target_cave not in self._get_neighbors(current_arrow_location) and target_cave != current_arrow_location:
                self.message = "Arrow veered off course! It hit nothing."
                valid_shot = False
                break

            current_arrow_location = target_cave

            if current_arrow_location == self.wumpus_location:
                self.message = "You shot the Wumpus! You win!"
                self.game_over = True
                return

            if current_arrow_location == self.player_location:
                self.message = "You shot yourself! Game Over."
                self.game_over = True
                return

        if not self.game_over and valid_shot:
            if random.random() < 0.2:
                self.message = "Your shot woke the Wumpus! He moved!"
                original_wumpus_location = self.wumpus_location
                available_caves = [
                    c for c in range(1, self.num_caves + 1)
                    if c != self.player_location and c != original_wumpus_location
                ]
                if available_caves:
                    self.wumpus_location = random.choice(available_caves)
                else:
                    self.wumpus_location = random.choice(
                        [c for c in range(1, self.num_caves + 1) if c != self.player_location]
                    )
            else:
                self.message = "Arrow missed."

            if self.num_arrows == 0 and not self.game_over:
                self.message += "\nYou are out of arrows! Game Over."
                self.game_over = True
                
class WumpusGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # configure the main window
        self.title("Hunt the Wumpus")
        self.geometry("900x750")
        
        self.buttons = []
        self.moves = 0
        self.currency = 9999999999999
        self.radar_uses_left = 0
        self.plank_uses_left = 0
        self.heavy_shoes_uses_left = 0
        self.bomb_uses_left = 0
        self.bomb_used_this_turn = False
        self.create_widgets()
        self.start_new_game()
        
    def create_widgets(self):
        # main frame
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # game UI frame (initially visible)
        self.main_game_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.main_game_frame.pack(fill="both", expand=True)

        # store UI frame (initially hidden)
        self.store_frame = ctk.CTkFrame(self.main_frame)
        self.create_store_widgets(self.store_frame)

        control_frame = ctk.CTkFrame(self.main_game_frame)
        control_frame.pack(pady=(10, 10), anchor="center")
        start_button = ctk.CTkButton(control_frame, text="Start New Game", command=self.start_new_game, corner_radius=8)
        start_button.pack(padx=5)
        
        # currency and store frame
        currency_store_frame = ctk.CTkFrame(self.main_game_frame, fg_color="transparent")
        currency_store_frame.pack(pady=(10, 10), padx=20, anchor="center")

        # currency label
        self.currency_label = ctk.CTkLabel(
            currency_store_frame, 
            text=f"Currency: {self.currency}", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.currency_label.pack(side="right", padx=4)

        # store button
        store_button = ctk.CTkButton(
            currency_store_frame,
            text="Open Store",
            command=self.open_store,
            corner_radius=8,
            fg_color="#219d48",
            hover_color="#000000"
        )
        store_button.pack(side="left", padx=4)

        # frame for cave buttons
        cave_frame = ctk.CTkFrame(self.main_game_frame, fg_color="transparent")
        cave_frame.pack(pady=10, padx=10, anchor="center")

        # caves
        for i in range(1, 21):
            button = ctk.CTkButton(
            cave_frame,
            text=str(i),
            width=50,
            height=50,
            corner_radius=10,
            font=ctk.CTkFont(size=20, weight="bold"),
            command=lambda cave=i: self.move_player_from_gui(cave)
            )
            row = (i - 1) // 5
            col = (i - 1) % 5
            button.grid(row=row, column=col, padx=5, pady=5)
            self.buttons.append(button)

        # frame for all action controls (shooting and abilities)
        action_controls_frame = ctk.CTkFrame(self.main_game_frame, fg_color="transparent")
        action_controls_frame.pack(pady=10, padx=20, anchor="center")

        # frame for shooting controls
        shoot_frame = ctk.CTkFrame(action_controls_frame)
        shoot_frame.pack(side="left", padx=(0, 10))

        shoot_label = ctk.CTkLabel(shoot_frame, text="Shoot Arrow to:", font=ctk.CTkFont(size=14))
        shoot_label.pack(side="left", padx=(10, 5))
        
        self.shoot_menu = ctk.CTkOptionMenu(shoot_frame, values=[" "], width=100)
        self.shoot_menu.pack(side="left", padx=5)

        shoot_button = ctk.CTkButton(shoot_frame, text="Shoot", command=self.shoot_arrow_from_gui, corner_radius=8)
        shoot_button.pack(side="left", padx=5)

        # frame for all tool controls
        self.tools_frame = ctk.CTkFrame(action_controls_frame)
        self.tools_frame.pack(pady=5, padx=20, anchor="center")
        self.tools_frame.columnconfigure(0, weight=1)

        # radar controls
        self.radar_control_frame = ctk.CTkFrame(self.tools_frame, fg_color="transparent")
        radar_label = ctk.CTkLabel(self.radar_control_frame, text="Radar Cave:", font=ctk.CTkFont(size=14))
        radar_label.pack(side="left", padx=(10, 5))
        
        self.radar_menu = ctk.CTkOptionMenu(self.radar_control_frame, values=[" "], width=100)
        self.radar_menu.pack(side="left", padx=5)

        self.radar_button = ctk.CTkButton(self.radar_control_frame, text="Use Radar", command=self.use_radar, corner_radius=8, state=tk.DISABLED)
        self.radar_button.pack(side="left", padx=5)
        
        # bomb controls
        self.bomb_control_frame = ctk.CTkFrame(self.tools_frame, fg_color="transparent")
        bomb_label = ctk.CTkLabel(self.bomb_control_frame, text="Bombs a random adjacent cave", font=ctk.CTkFont(size=14))
        bomb_label.pack(side="left", padx=(10, 5))
        self.bomb_button = ctk.CTkButton(self.bomb_control_frame, text="Use Bomb", command=self.use_bomb, corner_radius=8, state=tk.DISABLED)
        self.bomb_button.pack(side="left", padx=5)

        # instructions (non-editable)
        self.instructions_box = ctk.CTkTextbox(self.main_game_frame, wrap="word", width=550, height=95)
        self.instructions_box.pack(pady=5, padx=20, anchor="center")
        self.instructions_box.insert("0.0", self.get_initial_instructions())
        self.instructions_box.configure(state="disabled")

        # game messages
        self.message_box = ctk.CTkTextbox(self.main_game_frame, wrap="word", width=550, height=140)
        self.message_box.pack(pady=5, padx=20, anchor="center")

        self.exit_button = ctk.CTkButton(self.main_game_frame, text="Exit", command=self.quit, corner_radius=8, fg_color="#b00020")
        self.exit_button.pack(side="bottom", padx=20, pady=5)

    # store 
    def create_store_widgets(self, parent_frame):
        store_label = ctk.CTkLabel(parent_frame, text="Store", font=ctk.CTkFont(size=18, weight="bold"))
        store_label.pack(pady=(10, 5))

        radar_frame = ctk.CTkFrame(parent_frame)
        radar_frame.pack(pady=5, padx=10, fill="x")
        ctk.CTkLabel(radar_frame, text="Radar (2 uses)\nShows the contents of a cave you can move to.", anchor="center").pack(side="left", padx=5, expand=True)
        self.buy_radar_btn = ctk.CTkButton(
            radar_frame, 
            text="Buy (50)",
            command=lambda: self.buy_ability("radar"), 
            corner_radius=8,
            fg_color="#219d48",
            hover_color="#000000"
        )
        self.buy_radar_btn.pack(side="right", padx=5)
        self.radar_uses_label = ctk.CTkLabel(radar_frame, text=f"Uses Left: {self.radar_uses_left}")
        self.radar_uses_label.pack(side="right", padx=5)
        
        planks_frame = ctk.CTkFrame(parent_frame)
        planks_frame.pack(pady=5, padx=10, fill="x")
        ctk.CTkLabel(planks_frame, text="Wooden Planks (1 use)\nProtects you from those pesky pits.", anchor="center").pack(side="left", padx=5, expand=True)
        self.buy_planks_btn = ctk.CTkButton(
            planks_frame, 
            text="Buy (75)", 
            command=lambda: self.buy_ability("planks"), 
            corner_radius=8,
            fg_color="#219d48",
            hover_color="#000000"
        )
        self.buy_planks_btn.pack(side="right", padx=5)
        self.plank_uses_label = ctk.CTkLabel(planks_frame, text=f"Uses Left: {self.plank_uses_left}")
        self.plank_uses_label.pack(side="right", padx=5)
        
        heavy_shoes_frame = ctk.CTkFrame(parent_frame)
        heavy_shoes_frame.pack(pady=5, padx=10, fill="x")
        ctk.CTkLabel(heavy_shoes_frame, text="Heavy Shoes (1 use)\nBats will not be able to pick you up!", anchor="center").pack(side="left", padx=5, expand=True)
        self.buy_heavy_shoes_btn = ctk.CTkButton(
            heavy_shoes_frame, 
            text="Buy (60)", 
            command=lambda: self.buy_ability("heavy_shoes"), 
            corner_radius=8,
            fg_color="#219d48",
            hover_color="#000000"
        )
        self.buy_heavy_shoes_btn.pack(side="right", padx=5)
        self.heavy_shoes_uses_label = ctk.CTkLabel(heavy_shoes_frame, text=f"Uses Left: {self.heavy_shoes_uses_left}")
        self.heavy_shoes_uses_label.pack(side="right", padx=5)

        bomb_frame = ctk.CTkFrame(parent_frame)
        bomb_frame.pack(pady=5, padx=10, fill="x")
        ctk.CTkLabel(bomb_frame, text='Bomb (1 use per turn)\n"Clears out caves like a dream." - Random Miner', anchor="w").pack(side="left", padx=5, expand=True)
        self.buy_bomb_btn = ctk.CTkButton(
            bomb_frame, 
            text="Buy (100)", 
            command=lambda: self.buy_ability("bomb"), 
            corner_radius=8,
            fg_color="#219d48",
            hover_color="#000000"
        )
        self.buy_bomb_btn.pack(side="right", padx=5)
        self.bomb_uses_label = ctk.CTkLabel(bomb_frame, text=f"Uses Left: {self.bomb_uses_left}")
        self.bomb_uses_label.pack(side="right", padx=5)
        
        close_button = ctk.CTkButton(parent_frame, text="Close Store", command=self.close_store, corner_radius=8, fg_color="#b00020") 
        close_button.pack(pady=5, padx=20, anchor="center")

    def open_store(self):
        self.main_game_frame.pack_forget()
        self.store_frame.pack(fill="both", expand=True)
        self.exit_button.pack_forget()
        self.update_display()
            
    def close_store(self):
        self.store_frame.pack_forget()
        self.main_game_frame.pack(fill="both", expand=True)
        self.exit_button.pack(pady=10, padx=20, anchor="center")
        self.update_display()

    def buy_ability(self, ability):
        price_map = {"radar": 50, "planks": 75, "heavy_shoes": 60, "bomb": 100}
        price = price_map.get(ability)
        
        if self.currency >= price:
            self.currency -= price
            self.game.message = f"Purchased {ability.replace('_', ' ')} for {price} currency."
            if ability == "radar":
                self.radar_uses_left += 2
            elif ability == "planks":
                self.plank_uses_left += 1
            elif ability == "heavy_shoes":
                self.heavy_shoes_uses_left += 1
            elif ability == "bomb":
                self.bomb_uses_left += 1
        else:
            self.game.message = f"Not enough currency to buy {ability.replace('_', ' ')}."
            
        self.update_display()

    def start_new_game(self):
        # new game instance for the wumpus and hazards
        self.game = HuntTheWumpus(initial_arrows=5)
        self.moves = 0
        self.bomb_used_this_turn = False # reset the bomb usage flag

        
        self.game.message = "Starting a new game. Good luck!"
        self.update_display()

    def get_initial_instructions(self):
        return (
            "Welcome to Hunt the Wumpus!\n"
            "Objective: Hunt down the Wumpus without falling into pits or being carried by bats.\n"
            "To move, click on a connected cave button.\n"
            "To shoot, select a connected cave from the dropdown menu and click Shoot.\n"
            "Use currency earned to buy abilities in the store.\n"
        )
    
    def move_player_from_gui(self, destination):
        if self.game.game_over:
            return
        self.bomb_used_this_turn = False
        self.moves += 1
        hazard_check = self.game.move_player(destination, self.plank_uses_left > 0, self.heavy_shoes_uses_left > 0)
        
        if hazard_check == "planks":
            self.plank_uses_left -= 1
        elif hazard_check == "heavy_shoes":
            self.heavy_shoes_uses_left -= 1
        
        self.update_display()
        if hazard_check is True:
            messagebox.showinfo("Game Over", self.game.message)

    def shoot_arrow_from_gui(self):
        if self.game.game_over:
            return
        
        target_cave_str = self.shoot_menu.get()
        if target_cave_str and target_cave_str.strip() != " ":
            target_cave = int(target_cave_str)
            self.game.shoot_arrow([target_cave])
            
            if self.game.game_over and "You shot the Wumpus!" in self.game.message:
                self.award_currency()
                
            self.update_display()
            if self.game.game_over:
                messagebox.showinfo("Game Over", self.game.message)
        else:
            self.game.message = "You must select a cave to shoot at."
            self.update_display()

    def award_currency(self):
        reward = max(100 - (self.moves * 2), 10)
        self.currency += reward
        self.game.message += f"\n You won! You receive {reward} currency."

    def use_radar(self):
        if self.radar_uses_left > 0:
            target_cave_str = self.radar_menu.get()
            if target_cave_str and target_cave_str.strip() != " ":
                target_cave = int(target_cave_str)
                self.radar_uses_left -= 1
                self.game.message = self.check_cave_contents(target_cave)
                self.update_display()
            else:
                self.game.message = "Please select a cave to use the radar on."
                self.update_display()
        else:
            self.game.message = "You don't have any Radar uses left."
            self.update_display()

    def use_bomb(self):
        if self.game.game_over:
            self.game.message = "The game is over. Start a new game."
            self.update_display()
            return
        # check if a bomb has already been used this turn.
        if self.bomb_used_this_turn:
            self.game.message = "You can only use one bomb per turn. Move to a new cave to use another."
            self.update_display()
            return
            
        if self.bomb_uses_left > 0:
            neighbors = self.game._get_neighbors(self.game.player_location)
            if not neighbors:
                self.game.message = "There are no adjacent caves to drop a bomb on."
                self.update_display()
                return
            self.bomb_uses_left -= 1
            self.bomb_used_this_turn = True
            target_cave = random.choice(neighbors)
            self.game.message = f"You dropped a bomb on cave {target_cave}!\n"

            if target_cave == self.game.wumpus_location:
                self.game.message += "BOOM! The Wumpus was in that cave and is now gone!"
                self.game.wumpus_location = -1  # Wumpus is destroyed
            elif target_cave in self.game.pit_locations:
                self.game.message += "BOOM! A bottomless pit was in that cave and is now filled in!"
                self.game.pit_locations.remove(target_cave) # Pit is destroyed
            elif target_cave in self.game.bat_locations:
                self.game.message += "BOOM! Giant bats were in that cave and are now scattered!"
                self.game.bat_locations.remove(target_cave) # Bats are destroyed
            else:
                self.game.message += "The bomb hit an empty cave. It seems the obstacles were elsewhere."
            
            self.update_display()
        else:
            self.game.message = "You don't have any bombs left."
            self.update_display()
            
    def check_cave_contents(self, cave_num):
        if cave_num == self.game.wumpus_location:
            return f"Radar scan of cave {cave_num}: Wumpus is there!"
        elif cave_num in self.game.pit_locations:
            return f"Radar scan of cave {cave_num}: A bottomless pit is there."
        elif cave_num in self.game.bat_locations:
            return f"Radar scan of cave {cave_num}: Giant bats are there."
        else:
            return f"Radar scan of cave {cave_num}: It's empty."
    
    def update_display(self):
        self.currency_label.configure(text=f"Currency: {self.currency}")
        self.buy_radar_btn.configure(state=tk.NORMAL if self.currency >= 50 else tk.DISABLED)
        self.buy_planks_btn.configure(state=tk.NORMAL if self.currency >= 75 else tk.DISABLED)
        self.buy_heavy_shoes_btn.configure(state=tk.NORMAL if self.currency >= 60 else tk.DISABLED)
        self.buy_bomb_btn.configure(state=tk.NORMAL if self.currency >= 100 else tk.DISABLED)

        self.radar_uses_label.configure(text=f"Uses Left: {self.radar_uses_left}")
        self.plank_uses_label.configure(text=f"Uses Left: {self.plank_uses_left}")
        self.heavy_shoes_uses_label.configure(text=f"Uses Left: {self.heavy_shoes_uses_left}")
        self.bomb_uses_label.configure(text=f"Uses Left: {self.bomb_uses_left}")

        # clear the dynamic message box
        self.message_box.configure(state="normal")
        self.message_box.delete("0.0", "end")
        
        # game state information
        self.message_box.insert("end", f"--- Current State ---\n")
        self.message_box.insert("end", f"You are in cave {self.game.player_location}.\n")
        
        neighbors = self.game._get_neighbors(self.game.player_location)
        self.message_box.insert("end", f"Connected caves: {neighbors}\n")
        
        self.message_box.insert("end", f"Arrows remaining: {self.game.num_arrows}\n\n")

        # update shoot menu options
        neighbor_strings = [str(n) for n in neighbors]
        if not neighbor_strings:
            self.shoot_menu.configure(values=[" "], state=tk.DISABLED)
            self.shoot_menu.set(" ")
        else:
            self.shoot_menu.configure(values=neighbor_strings, state=tk.NORMAL)
            self.shoot_menu.set(neighbor_strings[0])

        # update tools frame visibility and its contents
        has_tools = self.radar_uses_left > 0 or self.bomb_uses_left > 0
        if has_tools:
            self.tools_frame.pack(pady=5, padx=20, anchor="center")
        else:
            self.tools_frame.pack_forget()

        # update radar menu options and visibility
        all_caves = [str(i) for i in range(1, 21)]
        if self.radar_uses_left > 0:
            self.radar_control_frame.pack(pady=5, padx=0)
            self.radar_menu.configure(values=all_caves, state=tk.NORMAL)
            self.radar_button.configure(state=tk.NORMAL)
            self.radar_menu.set(all_caves[0])
        else:
            self.radar_control_frame.pack_forget()
        
        # bomb button is disabled if you've already used one on current turn
        if self.bomb_uses_left > 0:
            self.bomb_control_frame.pack(pady=5, padx=0)
            if self.bomb_used_this_turn:
                self.bomb_button.configure(state=tk.DISABLED)
            else:
                self.bomb_button.configure(state=tk.NORMAL)
        else:
            self.bomb_control_frame.pack_forget()
        
        # perceptions
        perceptions = self.game._get_perceptions()
        for p in perceptions:
            self.message_box.insert("end", f"{p}\n")
        
        self.message_box.insert("end", f"\nMessage: {self.game.message}\n")
        self.message_box.configure(state="disabled")

        # update button colors for caves
        for i, button in enumerate(self.buttons):
            cave_num = i + 1
            if self.game.game_over:
                button.configure(fg_color="#1a1a1a", text_color="white", state=tk.DISABLED)
            elif cave_num == self.game.player_location:
                button.configure(fg_color="#34547c", text_color="white", state=tk.NORMAL)
            elif cave_num in neighbors:
                button.configure(fg_color="#3c6f4c", text_color="white", state=tk.NORMAL)
            else:
                button.configure(fg_color="#333333", text_color="white", state=tk.DISABLED)

if __name__ == '__main__':
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = WumpusGUI()
    app.mainloop()
