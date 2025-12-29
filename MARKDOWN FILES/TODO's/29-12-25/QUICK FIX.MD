# **VOXENT: How It Actually Works (Concise)**

## **Current Implementation Flow**

INPUT → BATCH PROCESSING → DIARIZATION → CLASSIFICATION → DATASET OUTPUT

---

## **1\. Input Stage 📥**

**Current behavior:**

* Scans `data/input_calls/` directory  
* Accepts: WAV files (MP3 auto-converts if you apply fixes)  
* Processes ALL files in directory sequentially  
* No batch sorting by duration

**Your desired behavior:**

\# NOT IMPLEMENTED YET \- Would need to add:  
def create\_duration\_batches(files):  
    batches \= {  
        'batch\_1': \[\],  \# 0-2 min  
        'batch\_2': \[\],  \# 2-4 min  
        'batch\_3': \[\],  \# 4-6 min  
        \# etc.  
    }  
      
    for file in files:  
        duration \= get\_audio\_duration(file)  
        if duration \<= 2:  
            batches\['batch\_1'\].append(file)  
        elif duration \<= 4:  
            batches\['batch\_2'\].append(file)  
        \# etc.  
      
    return batches

---

## **2\. Processing Pipeline ⚙️**

### **Step 2.1: Audio Preprocessing**

Raw audio → Load → Normalize → Remove silence → Mono 16kHz

### **Step 2.2: Speaker Diarization**

Audio → pyannote.audio → Identifies "who spoke when"

**Output example:**

\[  
  {speaker: "SPEAKER\_00", start: 0.0s, end: 3.2s},  
  {speaker: "SPEAKER\_01", start: 3.2s, end: 7.8s},  
  {speaker: "SPEAKER\_00", start: 7.8s, end: 12.1s}  
\]

### **Step 2.3: Extract Segments**

For each segment:  
  \- Cut audio \[start:end\]  
  \- Skip if \< 1 second

---

## **3\. Gender Classification 🎯**

**Current implementation:**

Audio segment → Pitch analysis → Male/Female/Uncertain

**Method:**

* Male: Pitch \< 85 Hz (typically 85-180 Hz)  
* Female: Pitch \> 165 Hz (typically 165-255 Hz)  
* Uncertain: Between 85-165 Hz

**Confidence scoring:**

* High confidence: \>80%  
* Medium: 60-80%  
* Low: \<60%

**Outputs 3 folders:**

data/voice\_dataset/  
├── male/          \# Male voice samples  
├── female/        \# Female voice samples  
└── uncertain/     \# Ambiguous samples

---

## **4\. File Naming Convention 📝**

**Current format:**

{original\_filename}\_spk{speaker\_number}\_conf{confidence}.wav

**Example:**

call\_123.wav → processes to:  
├── call\_123\_spk0\_conf87.wav  (male folder)  
├── call\_123\_spk1\_conf92.wav  (female folder)  
└── call\_123\_spk2\_conf45.wav  (uncertain folder)

**Your desired format:**

Suggested naming: voice\_sample\_001.wav, voice\_sample\_002.wav, etc.

To implement:

\# Add counter in dataset/organizer.py  
global\_counter \= 0

def save\_sample\_with\_counter(audio, sr, label, base\_path):  
    global global\_counter  
    global\_counter \+= 1  
    filename \= f"voice\_sample\_{global\_counter:04d}.wav"  
    \# Save with metadata linking to original

---

## **5\. Metadata Tracking 📊**

**Current metadata.csv:**

file,source,speaker,pitch,label,confidence,duration,quality\_score,snr  
voice\_sample\_0001.wav,call\_123.wav,SPEAKER\_00,120.5,male,87.3,3.2,78.5,15.2  
voice\_sample\_0002.wav,call\_123.wav,SPEAKER\_01,220.8,female,92.1,2.8,82.3,16.8

**Tracks:**

* Original source file  
* Speaker ID  
* Voice characteristics (pitch)  
* Classification result  
* Confidence score  
* Quality metrics

---

## **Missing Features vs Your Requirements**

| Your Requirement | Current Status | Implementation Needed |
| ----- | ----- | ----- |
| **Duration-based batching** | ❌ Missing | Add batch sorting logic |
| **Batch priority processing** | ❌ Missing | Process smallest batches first |
| **Voice separation (male/female)** | ✅ Implemented | Working |
| **Custom file naming** | ⚠️ Partial | Has naming, needs counter |
| **Dataset preparation** | ✅ Implemented | Organized folders \+ metadata |

---

## **What Needs to Change**

### **Add Duration-Based Batching**

\# Add to engine/batch\_runner.py

def process\_in\_batches(files, cfg):  
    """Process files in duration-sorted batches."""  
      
    \# 1\. Get durations  
    file\_durations \= \[\]  
    for file in files:  
        duration \= librosa.get\_duration(filename=file)  
        file\_durations.append((file, duration))  
      
    \# 2\. Create batches  
    batches \= {}  
    for file, duration in file\_durations:  
        batch\_key \= f"batch\_{int(duration // 2\) \+ 1}"  \# 0-2min, 2-4min, etc.  
        if batch\_key not in batches:  
            batches\[batch\_key\] \= \[\]  
        batches\[batch\_key\].append(file)  
      
    \# 3\. Process batches in order  
    results \= \[\]  
    for batch\_name in sorted(batches.keys()):  
        logger.info(f"Processing {batch\_name}: {len(batches\[batch\_name\])} files")  
        for file in batches\[batch\_name\]:  
            result \= process\_file(file, cfg)  
            results.append(result)  
      
    return results

### **Add Sequential Naming**

\# Update dataset/organizer.py

import json  
import os

COUNTER\_FILE \= "data/voice\_dataset/.counter.json"

def get\_next\_counter():  
    if os.path.exists(COUNTER\_FILE):  
        with open(COUNTER\_FILE, 'r') as f:  
            data \= json.load(f)  
            counter \= data.get('counter', 0\) \+ 1  
    else:  
        counter \= 1  
      
    with open(COUNTER\_FILE, 'w') as f:  
        json.dump({'counter': counter}, f)  
      
    return counter

def save\_sample(audio, sr, label, filename, base\_path):  
    counter \= get\_next\_counter()  
    new\_filename \= f"voice\_sample\_{counter:04d}.wav"  
      
    path \= os.path.join(base\_path, label)  
    os.makedirs(path, exist\_ok=True)  
    sf.write(os.path.join(path, new\_filename), audio, sr)  
      
    return new\_filename  \# Return for metadata

---

## **Quick Implementation Script**

\# quick\_changes.py \- Run this to add your requirements

def add\_duration\_batching():  
    """Add duration-based batch processing."""  
    \# Read batch\_runner.py  
    with open('engine/batch\_runner.py', 'r') as f:  
        content \= f.read()  
      
    \# Add batch function before run()  
    batch\_function \= '''  
def create\_duration\_batches(files):  
    """Sort files into batches by duration."""  
    import librosa  
      
    batches \= {}  
    for file in files:  
        try:  
            duration \= librosa.get\_duration(filename=file)  
            batch\_num \= int(duration // 2\) \+ 1  \# 2-minute intervals  
            batch\_key \= f"batch\_{batch\_num}"  
              
            if batch\_key not in batches:  
                batches\[batch\_key\] \= \[\]  
            batches\[batch\_key\].append(file)  
        except:  
            \# If duration fails, put in batch\_0  
            if 'batch\_0' not in batches:  
                batches\['batch\_0'\] \= \[\]  
            batches\['batch\_0'\].append(file)  
      
    return batches

'''  
      
    \# Insert before def run()  
    content \= content.replace('def run(config\_path):', batch\_function \+ '\\ndef run(config\_path):')  
      
    \# Modify run() to use batches  
    old\_code \= 'files \= \[os.path.join(input\_dir, f) for f in os.listdir(input\_dir) if f.endswith(".wav")\]'  
    new\_code \= '''files \= \[os.path.join(input\_dir, f) for f in os.listdir(input\_dir) if f.endswith(".wav")\]  
          
        \# Create duration-based batches  
        batches \= create\_duration\_batches(files)  
        logger.info(f"Created {len(batches)} batches")  
          
        \# Process batches in order (smallest first)  
        files \= \[\]  
        for batch\_key in sorted(batches.keys()):  
            logger.info(f"Batch {batch\_key}: {len(batches\[batch\_key\])} files")  
            files.extend(batches\[batch\_key\])'''  
      
    content \= content.replace(old\_code, new\_code)  
      
    with open('engine/batch\_runner.py', 'w') as f:  
        f.write(content)  
      
    print("✅ Added duration-based batching")

def add\_sequential\_naming():  
    """Add sequential file naming."""  
    organizer\_code \= '''import os  
import soundfile as sf  
import json

COUNTER\_FILE \= "data/voice\_dataset/.counter.json"

def get\_next\_counter():  
    """Get next sequential file number."""  
    if os.path.exists(COUNTER\_FILE):  
        with open(COUNTER\_FILE, 'r') as f:  
            counter \= json.load(f).get('counter', 0\) \+ 1  
    else:  
        counter \= 1  
      
    with open(COUNTER\_FILE, 'w') as f:  
        json.dump({'counter': counter}, f)  
      
    return counter

def save\_sample(audio, sr, label, filename, base\_path):  
    """Save sample with sequential naming."""  
    counter \= get\_next\_counter()  
    new\_filename \= f"voice\_sample\_{counter:04d}.wav"  
      
    path \= os.path.join(base\_path, label)  
    os.makedirs(path, exist\_ok=True)  
    sf.write(os.path.join(path, new\_filename), audio, sr)  
      
    \# Store original filename in metadata  
    return new\_filename  
'''  
      
    with open('dataset/organizer.py', 'w') as f:  
        f.write(organizer\_code)  
      
    print("✅ Added sequential file naming")

if \_\_name\_\_ \== "\_\_main\_\_":  
    add\_duration\_batching()  
    add\_sequential\_naming()  
    print("\\n✅ All changes applied\!")  
    print("\\n📝 Modified files:")  
    print("  \- engine/batch\_runner.py")  
    print("  \- dataset/organizer.py")

---

## **Usage After Changes**

\# 1\. Place audio files  
cp your\_calls/\*.wav data/input\_calls/

\# 2\. Run pipeline  
python config/run\_pipeline.py

\# 3\. Check output  
ls data/voice\_dataset/male/       \# voice\_sample\_0001.wav, 0002.wav, etc.  
ls data/voice\_dataset/female/     \# voice\_sample\_0003.wav, 0004.wav, etc.  
cat data/voice\_dataset/metadata.csv

---

## **Final Output Structure**

data/voice\_dataset/  
├── male/  
│   ├── voice\_sample\_0001.wav  (from call\_001.wav, SPEAKER\_00)  
│   ├── voice\_sample\_0003.wav  (from call\_001.wav, SPEAKER\_02)  
│   └── voice\_sample\_0005.wav  (from call\_002.wav, SPEAKER\_00)  
├── female/  
│   ├── voice\_sample\_0002.wav  (from call\_001.wav, SPEAKER\_01)  
│   └── voice\_sample\_0004.wav  (from call\_002.wav, SPEAKER\_01)  
├── uncertain/  
│   └── voice\_sample\_0006.wav  (low confidence)  
└── metadata.csv  (tracks original sources)
