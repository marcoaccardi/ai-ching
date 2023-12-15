from music21 import note, stream, metadata
import random
import itertools
from datetime import datetime
import os
import argparse


class GeneticMusic:
    def __init__(self, hexagram_number, base_duration, harmonicity_ratio):
        # Generate all 64 possible combinations of 6-character strings (hexagrams) using 'Y' and 'N'.
        # Each hexagram represents a unique pattern for generating musical motifs.
        self.hexagrams = [''.join(h)
                          for h in itertools.product('YN', repeat=6)]
        self.initial_hexagram = self.hexagrams[hexagram_number - 1]
        self.base_duration = base_duration
        self.modes = {
            # Ionian Mode (Major Scale)
            1: [60, 62, 64, 65, 67, 69, 71],
            2: [60, 62, 63, 65, 67, 69, 70],  # Dorian Mode # 60, 69
            3: [60, 61, 63, 65, 67, 68, 70],  # Phrygian Mode # 60, 61
            4: [60, 62, 64, 66, 67, 69, 71],  # Lydian Mode # 60, 66
            5: [60, 62, 64, 65, 67, 69, 70],  # Mixolydian Mode #60, 70
            # Aeolian Mode (Natural Minor Scale)
            6: [60, 62, 63, 65, 67, 68, 70],  # 60, 68

        }
        # Extended range for each mode
        self.extended_modes = {}
        for mode_key, mode_notes in self.modes.items():
            extended_notes = []
            # Add notes from two octaves down
            extended_notes += [note - 24 for note in mode_notes]
            # Add notes from the original octave
            extended_notes += mode_notes
            # # Add notes from one octave up
            # extended_notes += [note - 12 for note in mode_notes]
            self.extended_modes[mode_key] = extended_notes

        # Define preferred notes for each mode
        self.preferred_notes = {
            1: [60, 71],  # Ionian
            2: [60, 69],  # Dorian
            3: [60, 61],  # Phrygian
            4: [60, 66],  # Lydian
            5: [60, 70],  # Mixolydian
            6: [60, 68],  # Aeolian

        }
        self.harmonicity_ratio = harmonicity_ratio

    def generate_initial_population(self, size=10, mode=None):
        population = []
        for _ in range(size):
            # Select a random hexagram as the basis for a motif.
            hexagram = self.initial_hexagram
            print(hexagram)
            motif = []
            for char in hexagram:
                if char == 'Y':
                    # Choose a note from the mode
                    note = random.choice(self.modes[mode])
                else:
                    # Use -1 to represent a rest
                    note = -1
                motif.append(note)
            population.append(motif)
        return population

    def fitness_function(self, motif, mode):
        score = 0
        score += self.conformity_to_scale(motif, mode)
        score += self.melodic_interest(motif)
        score += self.rhythmic_complexity(motif)
        score += self.motivic_development_potential(motif)
        score += self.repetition_and_variation(motif)
        return score

    # Checks how many notes in the motif conform to the chosen musical mode
    def conformity_to_scale(self, motif, mode):
        scale_notes = set(self.modes[mode])
        return sum(1 for note in motif if note in scale_notes and note != -1)

    # Assesses the melodic structure by comparing steps and leaps.
    def melodic_interest(self, motif):
        intervals = []
        prev_note = None
        for note in motif:
            if note != -1:  # Ignore rests
                if prev_note is not None:
                    interval = abs(note - prev_note)
                    intervals.append(interval)
                prev_note = note

        # Scoring the intervals
        score = 0
        for interval in intervals:
            if interval == 1 or interval == 2:  # Step movement
                score += 1
            elif interval > 4:  # Leap movement
                score += 2
            else:  # Neither a step nor a significant leap
                score += 0.5

        # adjust the weights (1, 2, 0.5) as per your preference for steps and leaps
        return score

    # Evaluates the rhythmic diversity in the motif
    def rhythmic_complexity(self, motif):
        note_count = sum(1 for note in motif if note != -1)
        rest_count = sum(1 for note in motif if note == -1)

        # score based on the presence of both notes and rests
        return 1 if note_count > 0 and rest_count > 0 else 0

    # Checks if the motif contains both notes and rests

    def motivic_development_potential(self, motif):
        has_notes = any(note != -1 for note in motif)
        has_rests = any(note == -1 for note in motif)
        return 1 if has_notes and has_rests else 0

    # Rewards motifs with a balance between repetition and variation
    def repetition_and_variation(self, motif):
        unique_elements = len(set(motif))
        # Adjust the range based on your motif's possible diversity
        return 1 if 3 <= unique_elements <= 5 else 0

    # Selects the top half of the population based on fitness scores for breeding
    def select_parents(self, population, mode):
        sorted_population = sorted(
            population,
            key=lambda motif: self.fitness_function(motif, mode),
            reverse=True
        )
        return sorted_population[:len(sorted_population) // 2]

    def crossover(self, parent1, parent2, mode):
        crossover_point = random.randint(1, len(parent1) - 1)
        child = parent1[:crossover_point] + parent2[crossover_point:]

        # Introduce variety from extended modes in crossover
        child = [random.choice(self.extended_modes[mode])
                 if random.random() < 0.1 else note for note in child]
        return child

    def mutate(self, motif, mode, generation, max_generations, mutation_rate):
        mutation_point = random.randint(0, len(motif) - 1)
        mutation_choice = random.random()
        hexagram = self.initial_hexagram  # Choose a random hexagram
        print(hexagram)
        # Adjust mutation behavior based on the generation
        generation_factor = generation / max_generations

        # Harmonicity-based mutation
        consonant_intervals = [3, 4, 5, 7]  # More consonant intervals
        dissonant_intervals = [1, 2, 6]  # More dissonant intervals

        if self.harmonicity_ratio > mutation_rate:
            # Choose more from consonant intervals
            interval_choices = consonant_intervals
        else:
            # Choose more from random (dissonant) intervals
            interval_choices = dissonant_intervals

        # Apply mutation based on the selected interval set
        if random.random() < mutation_rate:
            interval = random.choice(interval_choices)
            motif = [(note + interval if note != -1 else note)
                     for note in motif]

        # Original mutation logic
        if motif[mutation_point] == -1:  # If it's a rest
            if hexagram[mutation_point] == 'Y':
                if mutation_choice < (0.5 + generation_factor * 0.2):
                    motif[mutation_point] = random.choice(self.modes[mode])
        else:  # If it's a note
            if hexagram[mutation_point] == 'Y':
                if mutation_choice < (0.3 + generation_factor * 0.2):
                    motif[mutation_point] = random.choice(self.modes[mode])
            else:
                if mutation_choice < 0.4:
                    motif[mutation_point] = -1
                else:
                    motif[mutation_point] = random.choice(
                        self.extended_modes[mode])

        return motif

    # Generates a new population from the current one using selection, crossover, and mutation.

    def generate_next_generation(self, current_generation, mode, generation, max_generations, mutation_rate):
        parents = self.select_parents(current_generation, mode)
        next_generation = []

        while len(next_generation) < len(current_generation):
            parent1, parent2 = random.sample(parents, 2)
            child = self.crossover(parent1, parent2, mode)
            child = self.mutate(child, mode, generation,
                                max_generations, mutation_rate)
            next_generation.append(child)

        return next_generation

    def run_genetic_algorithm(self, generations, population_size, mode, mutation_rate):
        population = self.generate_initial_population(population_size, mode)

        for generation in range(generations):
            population = sorted(population, key=lambda motif: self.fitness_function(
                motif, mode), reverse=True)
            population = self.generate_next_generation(
                population, mode, generation, generations, mutation_rate)

        return population

    # Converts a hexagram into a sequence of musical notes and rests based on the selected mode
    def hexagram_to_music(self, motif, mode, dynamic_ratio):
        extended_scale = self.extended_modes[mode]
        music_sequences = []

        for _ in range(3):  # Creating 3 parts for polyphony
            sequence = []
            for i, note_val in enumerate(motif):
                note_duration = self.determine_note_duration(note_val)
                if note_val != -1:
                    selected_note = random.choice(extended_scale)
                    dynamic_level = self.determine_dynamic_level(
                        self.initial_hexagram[i], dynamic_ratio)
                    n = note.Note(selected_note)
                    n.duration.quarterLength = note_duration
                    n.volume.velocity = dynamic_level
                    sequence.append(n)
                else:
                    r = note.Rest()
                    r.duration.quarterLength = note_duration
                    sequence.append(r)
            music_sequences.append(sequence)

        return music_sequences

    def determine_dynamic_level(self, hex_char, dynamic_ratio):
        high_dynamics = range(80, 120)
        low_dynamics = range(60, 80)
        if hex_char == 'Y':
            return random.choice(high_dynamics) if random.random() < dynamic_ratio else random.choice(low_dynamics)
        else:
            return random.choice(low_dynamics) if random.random() < dynamic_ratio else random.choice(high_dynamics)

    def determine_note_duration(self, note):
        if note != -1:  # If it's a note
            # Introduce more variation in note durations
            return self.base_duration * random.choice([1, 1.5, 2])
        else:  # If it's a rest
            return self.base_duration * random.choice([0.5, 0.75, 1])

    def create_music21_score(self, music_sequences):
        score = stream.Score()
        score.metadata = metadata.Metadata(title="Hexagram Music Composition")

        for i, sequence in enumerate(music_sequences):
            part = stream.Part()
            part.id = f'Part {i+1}'
            for music_note in sequence:
                part.append(music_note)
            score.append(part)
        return score

    # Save the score as a MIDI file
    def save_as_midi(self, music_sequences, id=0):
        # Generate a date prefix for the filename
        date_prefix = datetime.now().strftime("%Y%m%d")
        midi_dir = "midi_generation"
        os.makedirs(midi_dir, exist_ok=True)

        # Format the sequential number with leading zeros
        sequential_number = f"{id:02d}"
        filename = f"{date_prefix}_{sequential_number}_hexagram_music.mid"

        # Complete file path
        midi_path = os.path.join(midi_dir, filename)
        score = self.create_music21_score(music_sequences)
        score.write('midi', fp=midi_path)
        print(f"MIDI file saved as {midi_path}")

# Main


def main(generations, population_size, hexagram_number, base_duration, mutation_rate, harmonicity_ratio, dynamic_ratio):
    gm = GeneticMusic(hexagram_number, base_duration, harmonicity_ratio)
    mode = random.choice(list(gm.modes.keys()))

    final_motifs = gm.run_genetic_algorithm(
        generations=generations,
        population_size=population_size,
        mode=mode,
        mutation_rate=mutation_rate)

    for i, motif in enumerate(final_motifs):
        music_sequences = gm.hexagram_to_music(motif, mode, dynamic_ratio)
        gm.save_as_midi(music_sequences, id=i)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Genetic Music Algorithm')
    parser.add_argument('--generations', type=int,
                        required=True, help='Number of generations to run')
    parser.add_argument('--population', type=int,
                        required=True, help='Size of the population')
    parser.add_argument('--hexagram', type=int, required=True,
                        choices=range(1, 65), help='Hexagram number (1-64)')
    parser.add_argument('--base_duration', type=int,
                        required=True, help='Base duration for notes')
    parser.add_argument('--mutation_rate', type=float,
                        required=True, help='Mutation rate for genetic algorithm')
    parser.add_argument('--harmonicity_ratio', type=float,
                        required=True, help='Harmonicity ratio from 0 to 1')
    parser.add_argument('--dynamic_ratio', type=float, required=True,
                        help='Dynamic ratio for high and low dynamics')

    args = parser.parse_args()
    main(args.generations, args.population, args.hexagram, args.base_duration,
         args.mutation_rate, args.harmonicity_ratio, args.dynamic_ratio)
