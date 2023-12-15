# AI-CHING
This project uses a genetic algorithm to generate music based on the concepts of hexagrams and musical modes. It creatively explores the intersection of algorithmic composition and traditional music theory to create unique musical motifs.

The script uses a genetic algorithm to generate musical motifs based on hexagrams and musical modes. The process involves creating an initial population of motifs, evolving these motifs over several generations, and then converting the final motifs into music.

### How to run it
```bash
pip install -r requirements.txt
source venv/bin/activate
python3 genetic_ching4.py --generations 1000 --population 10 --hexagram 20 --base_duration 4 --mutation_rate 0.3 --harmonicity_ratio 0.3 --dynamic_ratio 0.8
```

## CODE OVERVIEW
**Class GeneticMusic**
Initialization (__init__):

It generates all 64 combinations of 6-character strings (hexagrams) using 'Y' and 'N', each representing a musical motif pattern.
Initializes musical modes (scales) and their extended versions for varied note selection.
Sets a base duration for notes, a harmonicity ratio, and preferred notes for each mode.
Initial Population Generation (generate_initial_population):

Creates an initial population of motifs based on a selected hexagram.
Fitness Function (fitness_function):

Calculates a fitness score for a motif, considering conformity to scale, melodic interest, rhythmic complexity, motivic development potential, and repetition/variation.
Fitness Metrics:

Functions like conformity_to_scale, melodic_interest, rhythmic_complexity, motivic_development_potential, and repetition_and_variation provide specific scoring criteria for motifs.
Parent Selection (select_parents):

Selects the top half of the population based on fitness scores for breeding.
Genetic Operations:

crossover: Combines two parent motifs at a random point.
mutate: Introduces mutations in motifs to add variation, influenced by the generation number and a mutation rate.
Generation Advancement (generate_next_generation):

Generates a new population from the current one using selection, crossover, and mutation.
Algorithm Execution (run_genetic_algorithm):

Runs the genetic algorithm for a specified number of generations with a given population size, mode, and mutation rate.
Music Conversion (hexagram_to_music):

Converts a hexagram into a sequence of musical notes and rests.
MIDI File Creation (create_music21_score, save_as_midi):

Creates a musical score and saves it as a MIDI file.

