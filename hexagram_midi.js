const fs = require("fs");
const path = require("path");
const m = require("max-api");
const { exec } = require("child_process");

const watchDirectory = path.join(__dirname, "midi_generation");
m.post(watchDirectory);
fs.watch(watchDirectory, (eventType, filename) => {
  if (eventType === "rename") {
    const filePath = path.join(watchDirectory, filename);
    if (fs.existsSync(filePath)) {
      console.log(`New file detected: ${filename}`);

      // Check if the file is a MIDI file
      if (path.extname(filename).toLowerCase() === ".mid") {
        // Send a message to Max to load and play the MIDI file
        m.outlet(filePath);
        m.post("midi");
      }
    }
  }
});

// Handler to list files
function listFiles() {
  fs.readdir(watchDirectory, (err, files) => {
    if (err) {
      m.post("Error reading directory:", err.message);
      return;
    }

    m.outlet("clear", "clear");
    m.outlet("location", watchDirectory);
    // Output each file name
    files.forEach((file) => {
      if (file !== ".DS_Store") {
        m.outlet("file", file);
      }
    });
  });
}

// Handler to list files manually
m.addHandler("list_files", () => {
  listFiles();
});

// Watch for new files and list all files if a new one is added
fs.watch(watchDirectory, (eventType, filename) => {
  if (eventType === "rename" && filename !== ".DS_Store") {
    m.post(`Change detected: ${filename}`);
    listFiles();
  }
});

m.post(`Watching for changes in: ${watchDirectory}`);

// Handler to execute the Python script
m.addHandler("generateMotifs", () => {
  exec("python3 genetic_ching2.py", (error, stdout, stderr) => {
    if (error) {
      m.post(`exec error: ${error}`);
      return;
    }

    m.post(`stdout: ${stdout}`);
    m.post(`stderr: ${stderr}`);
  });
});

// Handler to delete all files in the current directory
m.addHandler("deleteAllFiles", () => {
  fs.readdir(watchDirectory, (err, files) => {
    if (err) {
      m.post(`Error reading directory: ${err}`);
      throw err;
    }

    for (const file of files) {
      fs.unlink(path.join(watchDirectory, file), (err) => {
        if (err) {
          m.post(`Error deleting file: ${err}`);
          throw err;
        }
        m.post(`Deleted file: ${file}`);
      });
    }
  });
});

// This keeps the Node.js process open
m.post("Node.js script is running...");

m.addHandler(
  "generate",
  (
    generation,
    population,
    hexagram,
    baseDuration,
    mutation_rate,
    harmonicity,
    dynamics
  ) => {
    let envName = "generative-music"; // Name of your Python environment
    let pythonScriptPath = "./genetic_ching4.py"; // Path to your Python script

    // Concatenate the command into a single line
    let command =
      `source ${envName}/bin/activate && ` +
      `python3 ${pythonScriptPath} ` +
      `--generations ${generation} ` +
      `--population ${population} ` +
      `--hexagram ${hexagram} ` +
      `--base_duration ${baseDuration} ` +
      `--mutation_rate ${mutation_rate} ` +
      `--harmonicity_ratio ${harmonicity} ` +
      `--dynamic_ratio ${dynamics}`;

    exec(command, (err, stdout, stderr) => {
      if (err) {
        // Node couldn't execute the command
        m.post(`exec error: ${err}`);
        return;
      }

      // the *entire* stdout and stderr (buffered)
      m.post(`stdout: ${stdout}`);
      m.post(`stderr: ${stderr}`);
    });
  }
);
