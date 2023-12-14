# AI-CHING
This project uses a genetic algorithm to generate music based on the concepts of hexagrams and musical modes. It creatively explores the intersection of algorithmic composition and traditional music theory to create unique musical motifs.

The script uses a genetic algorithm to generate musical motifs based on hexagrams and musical modes. The process involves creating an initial population of motifs, evolving these motifs over several generations, and then converting the final motifs into music.

### Key Components
Class GeneticMusic: The core class that encapsulates all the functionalities of the genetic algorithm for music generation.

Hexagram Generation: Converts hexagram numbers into 6-character strings used to influence the motif generation.

Musical Modes: Defines various musical modes which determine the scale and notes used in the motifs.

Extended Modes: Expands the basic modes to include a wider range of notes for more variety.

Harmonicity Ratio: A parameter to balance between consonant and random intervals during mutation.

Fitness Function: Evaluates how 'fit' a motif is based on several musical aspects.

Population Management: Functions to generate initial populations, select parents, perform crossover, and mutate motifs.

Music Generation: Converts the final motifs into a sequence of musical notes and rests.

MIDI File Output: Functions to save the generated music as MIDI files.


### Features
**Hexagram-based** Motif Generation: Utilizes the I Ching hexagrams to create deterministic yet variable patterns for note selection.
**Musical Modes**: Integrates various musical modes (Ionian, Dorian, Phrygian, Lydian, Mixolydian, Aeolian) for scale adherence.
**Harmonicity Ratio**: Employs a harmonicity ratio to balance consonant and random intervals, influencing the mutation process.
**Fitness Evaluation**: Includes a multi-faceted fitness function assessing scale conformity, melodic interest, rhythmic complexity, and more.
**Mutation and Crossover**: Utilizes genetic algorithm techniques for evolving motifs over generations.

