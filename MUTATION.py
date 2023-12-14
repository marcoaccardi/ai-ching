# RANDOM
def mutate(self, motif, mode, generation, max_generations):
    mutation_point = random.randint(0, len(motif) - 1)
    mutation_choice = random.random()
    hexagram = random.choice(self.hexagrams)  # Choose a random hexagram
    print(hexagram)
    # Adjust mutation behavior based on the generation
    generation_factor = generation / max_generations

    if motif[mutation_point] == -1:  # If it's a rest
        if hexagram[mutation_point] == 'Y':
            # Higher chance to change rest to a note in later generations
            if mutation_choice < (0.5 + generation_factor * 0.2):
                motif[mutation_point] = random.choice(self.modes[mode])
    else:  # If it's a note
        if hexagram[mutation_point] == 'Y':
            # Chance to mutate to a different note increases over generations
            if mutation_choice < (0.3 + generation_factor * 0.2):
                motif[mutation_point] = random.choice(self.modes[mode])
        else:
            # Chance to mutate to a rest or extended scale note
            if mutation_choice < 0.4:
                motif[mutation_point] = -1
            else:
                motif[mutation_point] = random.choice(
                    self.extended_modes[mode])

    return motif

# HARMONIC


def mutate(self, motif, mode, generation, max_generations, mutation_rate=0.1):
    mutation_point = random.randint(0, len(motif) - 1)
    mutation_choice = random.random()
    hexagram = random.choice(self.hexagrams)  # Choose a random hexagram
    print(hexagram)
    # Adjust mutation behavior based on the generation
    generation_factor = generation / max_generations

    # New mutation logic based on mutation_rate
    if random.random() < mutation_rate:
        # Perfect fourth, fifth, etc.
        interval = random.choice([3, 4, 5, 7])
        motif = [(note + interval if note != -1 else note)
                 for note in motif]

    # Original mutation logic
    if motif[mutation_point] == -1:  # If it's a rest
        if hexagram[mutation_point] == 'Y':
            # Higher chance to change rest to a note in later generations
            if mutation_choice < (0.5 + generation_factor * 0.2):
                motif[mutation_point] = random.choice(self.modes[mode])
    else:  # If it's a note
        if hexagram[mutation_point] == 'Y':
            # Chance to mutate to a different note increases over generations
            if mutation_choice < (0.3 + generation_factor * 0.2):
                motif[mutation_point] = random.choice(self.modes[mode])
        else:
            # Chance to mutate to a rest or extended scale note
            if mutation_choice < 0.4:
                motif[mutation_point] = -1
            else:
                motif[mutation_point] = random.choice(
                    self.extended_modes[mode])

    return motif

# HARMONIC AND MIRROR


def mutate(self, motif, mode, generation, max_generations, mutation_rate=0.1):
    mutation_point = random.randint(0, len(motif) - 1)
    mutation_choice = random.random()
    hexagram = random.choice(self.hexagrams)  # Choose a random hexagram
    print(hexagram)
    # Adjust mutation behavior based on the generation
    generation_factor = generation / max_generations

    # New mutation logic based on mutation_rate
    if random.random() < mutation_rate:
        interval = random.choice([3, 4, 5, 7])  # Perfect fourth, fifth, etc.
        motif = [(note + interval if note != -1 else note) for note in motif]

    # Mirror Mutation
    if random.random() < mutation_rate:
        midpoint = len(motif) // 2
        for i in range(midpoint):
            motif[-(i+1)] = motif[i]

    # Original mutation logic
    if motif[mutation_point] == -1:  # If it's a rest
        if hexagram[mutation_point] == 'Y':
            # Higher chance to change rest to a note in later generations
            if mutation_choice < (0.5 + generation_factor * 0.2):
                motif[mutation_point] = random.choice(self.modes[mode])
    else:  # If it's a note
        if hexagram[mutation_point] == 'Y':
            # Chance to mutate to a different note increases over generations
            if mutation_choice < (0.3 + generation_factor * 0.2):
                motif[mutation_point] = random.choice(self.modes[mode])
        else:
            # Chance to mutate to a rest or extended scale note
            if mutation_choice < 0.4:
                motif[mutation_point] = -1
            else:
                motif[mutation_point] = random.choice(
                    self.extended_modes[mode])

    return motif
