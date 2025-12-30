cd "c:\Users\chall\Downloads\PROJECTS\Voxent or EchoForge\VOXENT" ; python src/scripts/run_full_test.py
OXENT" ; python src/scripts/run_full_test.py                                                                         

╔==================================================================================================╗
║                                                                                                  ║
║                  VOXENT - VOICE CLASSIFICATION PIPELINE - FULL TEST & EXECUTION                  ║
║                                                                                                  ║
╚==================================================================================================╝

====================================================================================================
  CHECKING DEPENDENCIES
====================================================================================================

  ✅ PyYAML
  ✅ librosa
  ✅ soundfile
  ✅ numpy
  ✅ scipy
  ✅ scikit-learn
  ✅ psutil
  ✅ tqdm
  ✅ PyTorch
     GPU: NVIDIA GeForce RTX 2050
     VRAM: 4.29 GB

✅ All dependencies available

====================================================================================================
  CHECKING CONFIGURATION
====================================================================================================

  ✅ Config loaded: src/config/config.yaml
     Sample Rate: 16000 Hz
     Device: auto
     Batch Size GPU: 8
     Max Workers: 2

====================================================================================================
  CHECKING INPUT DATA
====================================================================================================

  ✅ 23 audio files found:
     • CHENNURU SHREYA REDDY-2512041909.mp3 (2.46 MB)
     • CHENNURU SHREYA REDDY-2512041914.mp3 (0.45 MB)
     • CHENNURU SHREYA REDDY-2512041915.mp3 (1.36 MB)
     • CHENNURU SHREYA REDDY-2512142242.mp3 (6.56 MB)
     • CHENNURU SHREYA REDDY-2512142309.mp3 (0.86 MB)
     • CHENNURU SHREYA REDDY-2512142317.mp3 (1.14 MB)
     • CHENNURU SHREYA REDDY-2512142319.mp3 (0.85 MB)
     • SaveClip.App_AQMGdlsfbIp7x2NXYZ8wKYDI4cJebCC1am_SlMX33HZV2bFNDV-teg2M0n-PoCDozUg8TwjqdLzYfeN2ei9gB4NFznFPuoa1M
x7V8GU_mp3.mp3 (0.45 MB)                                                                                                  • SaveClip.App_AQMGdlsfbIp7x2NXYZ8wKYDI4cJebCC1am_SlMX33HZV2bFNDV-teg2M0n-PoCDozUg8TwjqdLzYfeN2ei9gB4NFznFPuoa1M
x7V8GU_mp3.wav (1.20 MB)                                                                                                  • SaveClip.App_AQNGxC8bWFDBf_Iz3MoSshZCuOHDVF_4M3Cta9NVxuDWRfhUDpKo51cdv7zk1INEiU8jwjV_mj23zg7n7WWatiDzew9jh57Cn
r7K7FE_mp3.mp3 (0.55 MB)                                                                                                  • SaveClip.App_AQNGxC8bWFDBf_Iz3MoSshZCuOHDVF_4M3Cta9NVxuDWRfhUDpKo51cdv7zk1INEiU8jwjV_mj23zg7n7WWatiDzew9jh57Cn
r7K7FE_mp3.wav (1.47 MB)                                                                                                  • SaveClip.App_AQNY-VBXQ0HoJbbRNj5uJ5BGv5CnBh0SfBBa-SqO2tXSSbq2u5soG4FUnBHyMy79T6P7hOqFzYgZ3KA6Q7MTI9euBK4PbHsEB
mYJrNg_mp3.mp3 (0.62 MB)                                                                                                  • SaveClip.App_AQNY-VBXQ0HoJbbRNj5uJ5BGv5CnBh0SfBBa-SqO2tXSSbq2u5soG4FUnBHyMy79T6P7hOqFzYgZ3KA6Q7MTI9euBK4PbHsEB
mYJrNg_mp3.wav (1.66 MB)                                                                                                  • SaveClip.App_AQOtF76z2pcjZsJ81Weobl6mUyRogrBBoISDTV4Ut9FCG2ar3O5WTcnHBEnI2_W5cdMEl9gbCmWQKap0Yb_Y0fKm6hMIdgjIP
yp7v0A_mp3.mp3 (0.83 MB)                                                                                                  • SaveClip.App_AQOtF76z2pcjZsJ81Weobl6mUyRogrBBoISDTV4Ut9FCG2ar3O5WTcnHBEnI2_W5cdMEl9gbCmWQKap0Yb_Y0fKm6hMIdgjIP
yp7v0A_mp3.wav (2.21 MB)                                                                                                  • SaveClip.App_AQPE6zNGrNOfgNmsSazKS7aKZWM7orc4x_kL0p8DNnLzkYGXVHjhIBUizMjtN1toOQVZyaZhA8cDsfoPI8_cvCkn5wSHmE44U
0UOusY_mp3.mp3 (0.58 MB)                                                                                                  • SaveClip.App_AQPE6zNGrNOfgNmsSazKS7aKZWM7orc4x_kL0p8DNnLzkYGXVHjhIBUizMjtN1toOQVZyaZhA8cDsfoPI8_cvCkn5wSHmE44U
0UOusY_mp3.wav (1.55 MB)                                                                                                  • SaveClip.App_AQPHd0BpHWrZQx5SPV3IqsOYRXFnPSg0uOWNG_fTqqbZAhekmA-hiPztX05TscDCldBU4VpHsxxmllpXY1ovIVV51m2oPyNtO
oA5Ns4_mp3.mp3 (0.69 MB)                                                                                                  • SaveClip.App_AQPHd0BpHWrZQx5SPV3IqsOYRXFnPSg0uOWNG_fTqqbZAhekmA-hiPztX05TscDCldBU4VpHsxxmllpXY1ovIVV51m2oPyNtO
oA5Ns4_mp3.wav (1.83 MB)                                                                                                  • SaveClip.App_AQPIygeuh5zlcgu5a1zl_QZWcZkPkGh46_T6y9Suuzg3PMaBa8sDX74vM7BqgGr5URYCULlvW71oE8MZBSpl_TaUgsYDdWAgn
i940nM_mp3.mp3 (0.51 MB)                                                                                                  • SaveClip.App_AQPIygeuh5zlcgu5a1zl_QZWcZkPkGh46_T6y9Suuzg3PMaBa8sDX74vM7BqgGr5URYCULlvW71oE8MZBSpl_TaUgsYDdWAgn
i940nM_mp3.wav (1.37 MB)                                                                                                  • SaveClip.App_AQPlyxJuQuh6hsbdi2KfxwwWWVvlyz1DtRoDVrovRH_SdFz3ytEKRgogMrAjN-eI000usFRBCjsVt7Wn8aINgBFoSJm3mzbch
dCtWvQ_mp3.mp3 (0.89 MB)                                                                                                  • SaveClip.App_AQPlyxJuQuh6hsbdi2KfxwwWWVvlyz1DtRoDVrovRH_SdFz3ytEKRgogMrAjN-eI000usFRBCjsVt7Wn8aINgBFoSJm3mzbch
dCtWvQ_mp3.wav (2.37 MB)                                                                                             
====================================================================================================
  CHECKING CLASSIFIERS
====================================================================================================

2025-12-30 13:26:33,905 - classification - INFO - 🚀 GPU detected: NVIDIA GeForce RTX 2050
2025-12-30 13:26:33,906 - classification - INFO -    VRAM: 4.29 GB
  ✅ Integrated Classifier
  ✅ Pitch-Based Classifier
  ✅ ML Classifier
  ✅ Advanced Multi-Feature Classifier

====================================================================================================
  RUNNING PIPELINE
====================================================================================================

2025-12-30 13:26:35,060 - __main__ - INFO - Starting pipeline execution...
2025-12-30 13:26:35,073 - engine.batch_runner - INFO - Configuration validation passed
2025-12-30 13:26:35,074 - engine.batch_runner - INFO - 🚀 GPU detected: NVIDIA GeForce RTX 2050
2025-12-30 13:26:35,080 - engine.batch_runner - INFO - Converting 15 MP3 files to WAV...
2025-12-30 13:26:37,704 - engine.batch_runner - INFO - Converted: CHENNURU SHREYA REDDY-2512041909.mp3 → CHENNURU SHR
EYA REDDY-2512041909.wav                                                                                             2025-12-30 13:26:37,823 - engine.batch_runner - INFO - Converted: CHENNURU SHREYA REDDY-2512041914.mp3 → CHENNURU SHR
EYA REDDY-2512041914.wav                                                                                             2025-12-30 13:26:37,963 - engine.batch_runner - INFO - Converted: CHENNURU SHREYA REDDY-2512041915.mp3 → CHENNURU SHR
EYA REDDY-2512041915.wav                                                                                             2025-12-30 13:26:38,359 - engine.batch_runner - INFO - Converted: CHENNURU SHREYA REDDY-2512142242.mp3 → CHENNURU SHR
EYA REDDY-2512142242.wav                                                                                             2025-12-30 13:26:38,543 - engine.batch_runner - INFO - Converted: CHENNURU SHREYA REDDY-2512142309.mp3 → CHENNURU SHR
EYA REDDY-2512142309.wav                                                                                             2025-12-30 13:26:38,719 - engine.batch_runner - INFO - Converted: CHENNURU SHREYA REDDY-2512142317.mp3 → CHENNURU SHR
EYA REDDY-2512142317.wav                                                                                             2025-12-30 13:26:38,852 - engine.batch_runner - INFO - Converted: CHENNURU SHREYA REDDY-2512142319.mp3 → CHENNURU SHR
EYA REDDY-2512142319.wav                                                                                             2025-12-30 13:26:38,854 - engine.batch_runner - INFO - Starting batch processing of 30 files (15 WAV, 15 MP3)
2025-12-30 13:26:38,855 - engine.batch_runner - INFO - Creating duration-based batches...
C:\Users\chall\Downloads\PROJECTS\Voxent or EchoForge\VOXENT\src\scripts\..\engine\batch_runner.py:48: FutureWarning:
 get_duration() keyword argument 'filename' has been renamed to 'path' in version 0.10.0.                                    This alias will be removed in version 1.0.
  duration = librosa.get_duration(filename=file_path)
2025-12-30 13:26:43,238 - engine.batch_runner - INFO -   batch_1: 26 files
2025-12-30 13:26:43,239 - engine.batch_runner - INFO -   batch_2: 2 files
2025-12-30 13:26:43,239 - engine.batch_runner - INFO -   batch_3: 2 files
2025-12-30 13:26:43,239 - engine.batch_runner - INFO - Created 3 batches based on audio duration
2025-12-30 13:26:43,239 - engine.batch_runner - INFO - Processing batch_1: 26 files
2025-12-30 13:26:43,239 - engine.batch_runner - INFO -   🚀 Using GPU acceleration for batch
2025-12-30 13:26:43,240 - preprocessing.source_separator - INFO - Loading Demucs model 'htdemucs' on cpu...
2025-12-30 13:26:44,155 - preprocessing.source_separator - INFO - Demucs model loaded successfully
2025-12-30 13:26:44,157 - engine.batch_runner - INFO - Processing file: CHENNURU SHREYA REDDY-2512041914.wav
2025-12-30 13:26:44,157 - engine.batch_runner - INFO - Configuration validation passed
2025-12-30 13:26:44,158 - classification - INFO - ℹ️  ML model not found at models/ml_gender_classifier.pkl
2025-12-30 13:26:44,158 - classification.advanced_gender_classifier - INFO - Using MultiFeatureGenderClassifier (with
 formants)                                                                                                           2025-12-30 13:26:44,158 - classification - INFO - ✅ Advanced multi-feature classifier loaded
2025-12-30 13:26:44,158 - classification - INFO - Classifier initialized on cuda
2025-12-30 13:26:44,159 - classification - INFO - Classification priority: Advanced Multi-Feature Classifier → Pitch-
Based Classifier (fallback)                                                                                          2025-12-30 13:26:44,159 - engine.batch_runner - INFO - Processing file: CHENNURU SHREYA REDDY-2512041915.wav
2025-12-30 13:26:44,161 - engine.batch_runner - INFO - Configuration validation passed
Processing files:   0%|                                                                      | 0/26 [00:00<?, ?it/s]2
025-12-30 13:26:48,979 - engine.batch_runner - INFO - Separating vocals from accompaniment...                        2025-12-30 13:26:48,987 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:26:49,017 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:26:49,018 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:26:49,019 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:26:49,026 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:26:51,851 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:26:52,672 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:26:52,855 - engine.batch_runner - INFO - Successfully processed data/input\CHENNURU SHREYA REDDY-251204
1914.wav: 0 tracks in 7.70s                                                                                          2025-12-30 13:26:52,855 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:26:52,855 - engine.batch_runner - INFO - Processing file: CHENNURU SHREYA REDDY-2512142309.wav
2025-12-30 13:26:52,855 - engine.batch_runner - INFO - Configuration validation passed
Processing files:   4%|██▍                                                           | 1/26 [00:08<03:37,  8.69s/it]2
025-12-30 13:26:53,676 - engine.batch_runner - INFO - Successfully processed data/input\CHENNURU SHREYA REDDY-2512041915.wav: 0 tracks in 8.52s                                                                                           2025-12-30 13:26:53,676 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:26:53,677 - engine.batch_runner - INFO - Processing file: CHENNURU SHREYA REDDY-2512142317.wav
Processing files:   8%|████▊                                                         | 2/26 [00:09<01:37,  4.06s/it]2
025-12-30 13:26:53,678 - engine.batch_runner - INFO - Configuration validation passed                                2025-12-30 13:26:53,878 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:26:53,880 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:26:53,882 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:26:54,867 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:26:54,870 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:26:54,872 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:26:56,606 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:26:57,253 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:26:57,612 - engine.batch_runner - INFO - Successfully processed data/input\CHENNURU SHREYA REDDY-251214
2309.wav: 0 tracks in 3.76s                                                                                          2025-12-30 13:26:57,613 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:26:57,614 - engine.batch_runner - INFO - Processing file: CHENNURU SHREYA REDDY-2512142319.wav
Processing files:  12%|███████▏                                                      | 3/26 [00:13<01:32,  4.01s/it]2
025-12-30 13:26:57,614 - engine.batch_runner - INFO - Configuration validation passed                                2025-12-30 13:26:58,259 - engine.batch_runner - INFO - Successfully processed data/input\CHENNURU SHREYA REDDY-251214
2317.wav: 0 tracks in 3.58s                                                                                          2025-12-30 13:26:58,262 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:26:58,266 - engine.batch_runner - INFO - Processing file: SaveClip.App_AQMGdlsfbIp7x2NXYZ8wKYDI4cJebCC1
am_SlMX33HZV2bFNDV-teg2M0n-PoCDozUg8TwjqdLzYfeN2ei9gB4NFznFPuoa1Mx7V8GU_mp3.wav                                      Processing files:  15%|█████████▌                                                    | 4/26 [00:14<00:58,  2.68s/it]2
025-12-30 13:26:58,266 - engine.batch_runner - INFO - Configuration validation passed                                2025-12-30 13:26:58,622 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:26:58,623 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:26:58,625 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:26:59,295 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:26:59,388 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:26:59,435 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:27:01,215 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:27:01,222 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:27:02,218 - engine.batch_runner - INFO - Successfully processed data/input\SaveClip.App_AQMGdlsfbIp7x2N
XYZ8wKYDI4cJebCC1am_SlMX33HZV2bFNDV-teg2M0n-PoCDozUg8TwjqdLzYfeN2ei9gB4NFznFPuoa1Mx7V8GU_mp3.wav: 0 tracks in 2.95s  2025-12-30 13:27:02,218 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:27:02,219 - engine.batch_runner - INFO - Processing file: SaveClip.App_AQNGxC8bWFDBf_Iz3MoSshZCuOHDVF_4
M3Cta9NVxuDWRfhUDpKo51cdv7zk1INEiU8jwjV_mj23zg7n7WWatiDzew9jh57Cnr7K7FE_mp3.wav                                      Processing files:  19%|███████████▉                                                  | 5/26 [00:18<01:05,  3.14s/it]2
025-12-30 13:27:02,219 - engine.batch_runner - INFO - Configuration validation passed                                2025-12-30 13:27:02,225 - engine.batch_runner - INFO - Successfully processed data/input\CHENNURU SHREYA REDDY-251214
2319.wav: 0 tracks in 3.61s                                                                                          2025-12-30 13:27:02,225 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0} 
2025-12-30 13:27:02,225 - engine.batch_runner - INFO - Processing file: SaveClip.App_AQNY-VBXQ0HoJbbRNj5uJ5BGv5CnBh0S
fBBa-SqO2tXSSbq2u5soG4FUnBHyMy79T6P7hOqFzYgZ3KA6Q7MTI9euBK4PbHsEBmYJrNg_mp3.wav                                      2025-12-30 13:27:02,225 - engine.batch_runner - INFO - Configuration validation passed
2025-12-30 13:27:03,236 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:27:03,238 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:27:03,238 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:27:03,241 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:27:03,241 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:27:03,242 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:27:06,411 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:27:06,456 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:27:07,414 - engine.batch_runner - INFO - Successfully processed data/input\SaveClip.App_AQNGxC8bWFDBf_I
z3MoSshZCuOHDVF_4M3Cta9NVxuDWRfhUDpKo51cdv7zk1INEiU8jwjV_mj23zg7n7WWatiDzew9jh57Cnr7K7FE_mp3.wav: 0 tracks in 4.19s  2025-12-30 13:27:07,414 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:27:07,415 - engine.batch_runner - INFO - Processing file: SaveClip.App_AQOtF76z2pcjZsJ81Weobl6mUyRogrBB
oISDTV4Ut9FCG2ar3O5WTcnHBEnI2_W5cdMEl9gbCmWQKap0Yb_Y0fKm6hMIdgjIPyp7v0A_mp3.wav                                      Processing files:  27%|████████████████▋                                             | 7/26 [00:23<00:54,  2.86s/it]2
025-12-30 13:27:07,415 - engine.batch_runner - INFO - Configuration validation passed                                2025-12-30 13:27:07,459 - engine.batch_runner - INFO - Successfully processed data/input\SaveClip.App_AQNY-VBXQ0HoJbb
RNj5uJ5BGv5CnBh0SfBBa-SqO2tXSSbq2u5soG4FUnBHyMy79T6P7hOqFzYgZ3KA6Q7MTI9euBK4PbHsEBmYJrNg_mp3.wav: 0 tracks in 4.23s  2025-12-30 13:27:07,459 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:27:07,460 - engine.batch_runner - INFO - Processing file: SaveClip.App_AQPE6zNGrNOfgNmsSazKS7aKZWM7orc4
x_kL0p8DNnLzkYGXVHjhIBUizMjtN1toOQVZyaZhA8cDsfoPI8_cvCkn5wSHmE44U0UOusY_mp3.wav                                      2025-12-30 13:27:07,460 - engine.batch_runner - INFO - Configuration validation passed
2025-12-30 13:27:08,430 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:27:08,431 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:27:08,434 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:27:08,470 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:27:08,475 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:27:08,479 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:27:12,137 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:27:12,308 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:27:13,140 - engine.batch_runner - INFO - Successfully processed data/input\SaveClip.App_AQPE6zNGrNOfgNm
sSazKS7aKZWM7orc4x_kL0p8DNnLzkYGXVHjhIBUizMjtN1toOQVZyaZhA8cDsfoPI8_cvCkn5wSHmE44U0UOusY_mp3.wav: 0 tracks in 4.68s  2025-12-30 13:27:13,140 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:27:13,141 - engine.batch_runner - INFO - Processing file: SaveClip.App_AQPHd0BpHWrZQx5SPV3IqsOYRXFnPSg0
uOWNG_fTqqbZAhekmA-hiPztX05TscDCldBU4VpHsxxmllpXY1ovIVV51m2oPyNtOoA5Ns4_mp3.wav                                      Processing files:  35%|█████████████████████▍                                        | 9/26 [00:28<00:48,  2.86s/it]2
025-12-30 13:27:13,141 - engine.batch_runner - INFO - Configuration validation passed                                2025-12-30 13:27:13,313 - engine.batch_runner - INFO - Successfully processed data/input\SaveClip.App_AQOtF76z2pcjZsJ
81Weobl6mUyRogrBBoISDTV4Ut9FCG2ar3O5WTcnHBEnI2_W5cdMEl9gbCmWQKap0Yb_Y0fKm6hMIdgjIPyp7v0A_mp3.wav: 0 tracks in 4.90s  2025-12-30 13:27:13,313 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:27:13,314 - engine.batch_runner - INFO - Processing file: SaveClip.App_AQPIygeuh5zlcgu5a1zl_QZWcZkPkGh4
6_T6y9Suuzg3PMaBa8sDX74vM7BqgGr5URYCULlvW71oE8MZBSpl_TaUgsYDdWAgni940nM_mp3.wav                                      Processing files:  38%|███████████████████████▍                                     | 10/26 [00:29<00:35,  2.24s/it]2
025-12-30 13:27:13,314 - engine.batch_runner - INFO - Configuration validation passed                                2025-12-30 13:27:14,171 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:27:14,172 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:27:14,174 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:27:14,780 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:27:14,878 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:27:14,923 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:27:17,200 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:27:17,277 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:27:18,203 - engine.batch_runner - INFO - Successfully processed data/input\SaveClip.App_AQPIygeuh5zlcgu
5a1zl_QZWcZkPkGh46_T6y9Suuzg3PMaBa8sDX74vM7BqgGr5URYCULlvW71oE8MZBSpl_TaUgsYDdWAgni940nM_mp3.wav: 0 tracks in 3.89s  2025-12-30 13:27:18,203 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:27:18,204 - engine.batch_runner - INFO - Processing file: SaveClip.App_AQPlyxJuQuh6hsbdi2KfxwwWWVvlyz1D
tRoDVrovRH_SdFz3ytEKRgogMrAjN-eI000usFRBCjsVt7Wn8aINgBFoSJm3mzbchdCtWvQ_mp3.wav                                      Processing files:  42%|█████████████████████████▊                                   | 11/26 [00:34<00:43,  2.90s/it]2
025-12-30 13:27:18,204 - engine.batch_runner - INFO - Configuration validation passed                                2025-12-30 13:27:18,279 - engine.batch_runner - INFO - Successfully processed data/input\SaveClip.App_AQPHd0BpHWrZQx5
SPV3IqsOYRXFnPSg0uOWNG_fTqqbZAhekmA-hiPztX05TscDCldBU4VpHsxxmllpXY1ovIVV51m2oPyNtOoA5Ns4_mp3.wav: 0 tracks in 4.14s  2025-12-30 13:27:18,279 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:27:18,280 - engine.batch_runner - INFO - Processing file: CHENNURU SHREYA REDDY-2512041914.mp3
2025-12-30 13:27:18,280 - engine.batch_runner - INFO - Configuration validation passed
2025-12-30 13:27:19,226 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:27:19,228 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:27:19,231 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:27:19,307 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:27:19,308 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:27:19,309 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:27:21,822 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:27:22,488 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:27:22,824 - engine.batch_runner - INFO - Successfully processed data/input\CHENNURU SHREYA REDDY-251204
1914.mp3: 0 tracks in 3.54s                                                                                          2025-12-30 13:27:22,824 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:27:22,825 - engine.batch_runner - INFO - Processing file: CHENNURU SHREYA REDDY-2512041915.mp3
Processing files:  50%|██████████████████████████████▌                              | 13/26 [00:38<00:34,  2.66s/it]2
025-12-30 13:27:22,825 - engine.batch_runner - INFO - Configuration validation passed                                2025-12-30 13:27:23,492 - engine.batch_runner - INFO - Successfully processed data/input\SaveClip.App_AQPlyxJuQuh6hsb
di2KfxwwWWVvlyz1DtRoDVrovRH_SdFz3ytEKRgogMrAjN-eI000usFRBCjsVt7Wn8aINgBFoSJm3mzbchdCtWvQ_mp3.wav: 0 tracks in 4.29s  2025-12-30 13:27:23,492 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:27:23,493 - engine.batch_runner - INFO - Processing file: CHENNURU SHREYA REDDY-2512142309.mp3
Processing files:  54%|████████████████████████████████▊                            | 14/26 [00:39<00:26,  2.20s/it]2
025-12-30 13:27:23,493 - engine.batch_runner - INFO - Configuration validation passed                                2025-12-30 13:27:23,876 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:27:23,878 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:27:23,880 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:27:24,689 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:27:24,738 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:27:24,770 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:27:27,369 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:27:27,544 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:27:28,373 - engine.batch_runner - INFO - Successfully processed data/input\CHENNURU SHREYA REDDY-251214
2309.mp3: 0 tracks in 3.88s                                                                                          2025-12-30 13:27:28,373 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:27:28,373 - engine.batch_runner - INFO - Processing file: CHENNURU SHREYA REDDY-2512142317.mp3
2025-12-30 13:27:28,374 - engine.batch_runner - INFO - Configuration validation passed
Processing files:  58%|███████████████████████████████████▏                         | 15/26 [00:44<00:31,  2.86s/it]2
025-12-30 13:27:28,547 - engine.batch_runner - INFO - Successfully processed data/input\CHENNURU SHREYA REDDY-2512041915.mp3: 0 tracks in 4.72s                                                                                           2025-12-30 13:27:28,547 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:27:28,548 - engine.batch_runner - INFO - Processing file: CHENNURU SHREYA REDDY-2512142319.mp3
Processing files:  62%|█████████████████████████████████████▌                       | 16/26 [00:44<00:21,  2.16s/it]2
025-12-30 13:27:28,549 - engine.batch_runner - INFO - Configuration validation passed                                2025-12-30 13:27:29,409 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:27:29,410 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:27:29,412 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:27:30,011 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:27:30,100 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:27:30,131 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:27:32,253 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:27:32,306 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:27:33,256 - engine.batch_runner - INFO - Successfully processed data/input\CHENNURU SHREYA REDDY-251214
2319.mp3: 0 tracks in 3.71s                                                                                          2025-12-30 13:27:33,256 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:27:33,256 - engine.batch_runner - INFO - Processing file: SaveClip.App_AQMGdlsfbIp7x2NXYZ8wKYDI4cJebCC1
am_SlMX33HZV2bFNDV-teg2M0n-PoCDozUg8TwjqdLzYfeN2ei9gB4NFznFPuoa1Mx7V8GU_mp3.mp3                                      Processing files:  65%|███████████████████████████████████████▉                     | 17/26 [00:49<00:25,  2.85s/it]2
025-12-30 13:27:33,257 - engine.batch_runner - INFO - Configuration validation passed                                2025-12-30 13:27:33,310 - engine.batch_runner - INFO - Successfully processed data/input\CHENNURU SHREYA REDDY-251214
2317.mp3: 0 tracks in 3.94s                                                                                          2025-12-30 13:27:33,310 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:27:33,311 - engine.batch_runner - INFO - Processing file: SaveClip.App_AQNGxC8bWFDBf_Iz3MoSshZCuOHDVF_4
M3Cta9NVxuDWRfhUDpKo51cdv7zk1INEiU8jwjV_mj23zg7n7WWatiDzew9jh57Cnr7K7FE_mp3.mp3                                      2025-12-30 13:27:33,311 - engine.batch_runner - INFO - Configuration validation passed
2025-12-30 13:27:34,302 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:27:34,303 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:27:34,304 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:27:34,353 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:27:34,356 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:27:34,359 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:27:36,615 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:27:36,757 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:27:37,618 - engine.batch_runner - INFO - Successfully processed data/input\SaveClip.App_AQMGdlsfbIp7x2N
XYZ8wKYDI4cJebCC1am_SlMX33HZV2bFNDV-teg2M0n-PoCDozUg8TwjqdLzYfeN2ei9gB4NFznFPuoa1Mx7V8GU_mp3.mp3: 0 tracks in 3.36s  2025-12-30 13:27:37,618 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:27:37,618 - engine.batch_runner - INFO - Processing file: SaveClip.App_AQNY-VBXQ0HoJbbRNj5uJ5BGv5CnBh0S
fBBa-SqO2tXSSbq2u5soG4FUnBHyMy79T6P7hOqFzYgZ3KA6Q7MTI9euBK4PbHsEBmYJrNg_mp3.mp3                                      2025-12-30 13:27:37,619 - engine.batch_runner - INFO - Configuration validation passed
Processing files:  73%|████████████████████████████████████████████▌                | 19/26 [00:53<00:17,  2.56s/it]2
025-12-30 13:27:37,759 - engine.batch_runner - INFO - Successfully processed data/input\SaveClip.App_AQNGxC8bWFDBf_Iz3MoSshZCuOHDVF_4M3Cta9NVxuDWRfhUDpKo51cdv7zk1INEiU8jwjV_mj23zg7n7WWatiDzew9jh57Cnr7K7FE_mp3.mp3: 0 tracks in 3.45s   2025-12-30 13:27:37,759 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:27:37,760 - engine.batch_runner - INFO - Processing file: SaveClip.App_AQOtF76z2pcjZsJ81Weobl6mUyRogrBB
oISDTV4Ut9FCG2ar3O5WTcnHBEnI2_W5cdMEl9gbCmWQKap0Yb_Y0fKm6hMIdgjIPyp7v0A_mp3.mp3                                      Processing files:  77%|██████████████████████████████████████████████▉              | 20/26 [00:53<00:11,  1.98s/it]2
025-12-30 13:27:37,760 - engine.batch_runner - INFO - Configuration validation passed                                2025-12-30 13:27:38,665 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:27:38,666 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:27:38,668 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:27:39,235 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:27:39,332 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:27:39,378 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:27:41,870 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:27:42,304 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:27:42,873 - engine.batch_runner - INFO - Successfully processed data/input\SaveClip.App_AQNY-VBXQ0HoJbb
RNj5uJ5BGv5CnBh0SfBBa-SqO2tXSSbq2u5soG4FUnBHyMy79T6P7hOqFzYgZ3KA6Q7MTI9euBK4PbHsEBmYJrNg_mp3.mp3: 0 tracks in 4.25s  2025-12-30 13:27:42,873 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:27:42,874 - engine.batch_runner - INFO - Processing file: SaveClip.App_AQPE6zNGrNOfgNmsSazKS7aKZWM7orc4
x_kL0p8DNnLzkYGXVHjhIBUizMjtN1toOQVZyaZhA8cDsfoPI8_cvCkn5wSHmE44U0UOusY_mp3.mp3                                      2025-12-30 13:27:42,874 - engine.batch_runner - INFO - Configuration validation passed
Processing files:  81%|█████████████████████████████████████████████████▎           | 21/26 [00:58<00:13,  2.78s/it]2
025-12-30 13:27:43,307 - engine.batch_runner - INFO - Successfully processed data/input\SaveClip.App_AQOtF76z2pcjZsJ81Weobl6mUyRogrBBoISDTV4Ut9FCG2ar3O5WTcnHBEnI2_W5cdMEl9gbCmWQKap0Yb_Y0fKm6hMIdgjIPyp7v0A_mp3.mp3: 0 tracks in 4.55s   2025-12-30 13:27:43,307 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:27:43,308 - engine.batch_runner - INFO - Processing file: SaveClip.App_AQPHd0BpHWrZQx5SPV3IqsOYRXFnPSg0
uOWNG_fTqqbZAhekmA-hiPztX05TscDCldBU4VpHsxxmllpXY1ovIVV51m2oPyNtOoA5Ns4_mp3.mp3                                      Processing files:  85%|███████████████████████████████████████████████████▌         | 22/26 [00:59<00:08,  2.15s/it]2
025-12-30 13:27:43,308 - engine.batch_runner - INFO - Configuration validation passed                                2025-12-30 13:27:43,919 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:27:43,920 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:27:43,922 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:27:44,468 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:27:44,548 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:27:44,595 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:27:47,022 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:27:47,075 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:27:48,025 - engine.batch_runner - INFO - Successfully processed data/input\SaveClip.App_AQPE6zNGrNOfgNm
sSazKS7aKZWM7orc4x_kL0p8DNnLzkYGXVHjhIBUizMjtN1toOQVZyaZhA8cDsfoPI8_cvCkn5wSHmE44U0UOusY_mp3.mp3: 0 tracks in 4.15s  2025-12-30 13:27:48,025 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:27:48,026 - engine.batch_runner - INFO - Processing file: SaveClip.App_AQPIygeuh5zlcgu5a1zl_QZWcZkPkGh4
6_T6y9Suuzg3PMaBa8sDX74vM7BqgGr5URYCULlvW71oE8MZBSpl_TaUgsYDdWAgni940nM_mp3.mp3                                      Processing files:  88%|█████████████████████████████████████████████████████▉       | 23/26 [01:03<00:08,  2.86s/it]2
025-12-30 13:27:48,027 - engine.batch_runner - INFO - Configuration validation passed                                2025-12-30 13:27:48,080 - engine.batch_runner - INFO - Successfully processed data/input\SaveClip.App_AQPHd0BpHWrZQx5
SPV3IqsOYRXFnPSg0uOWNG_fTqqbZAhekmA-hiPztX05TscDCldBU4VpHsxxmllpXY1ovIVV51m2oPyNtOoA5Ns4_mp3.mp3: 0 tracks in 3.77s  2025-12-30 13:27:48,080 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:27:48,081 - engine.batch_runner - INFO - Processing file: SaveClip.App_AQPlyxJuQuh6hsbdi2KfxwwWWVvlyz1D
tRoDVrovRH_SdFz3ytEKRgogMrAjN-eI000usFRBCjsVt7Wn8aINgBFoSJm3mzbchdCtWvQ_mp3.mp3                                      2025-12-30 13:27:48,081 - engine.batch_runner - INFO - Configuration validation passed
2025-12-30 13:27:49,682 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:27:49,683 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:27:49,685 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:27:50,132 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:27:50,239 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:27:50,286 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:27:52,928 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:27:53,040 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:27:53,934 - engine.batch_runner - INFO - Successfully processed data/input\SaveClip.App_AQPIygeuh5zlcgu
5a1zl_QZWcZkPkGh46_T6y9Suuzg3PMaBa8sDX74vM7BqgGr5URYCULlvW71oE8MZBSpl_TaUgsYDdWAgni940nM_mp3.mp3: 0 tracks in 4.91s  2025-12-30 13:27:53,935 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
Processing files:  96%|██████████████████████████████████████████████████████████▋  | 25/26 [01:09<00:02,  2.90s/it]2
025-12-30 13:27:54,044 - engine.batch_runner - INFO - Successfully processed data/input\SaveClip.App_AQPlyxJuQuh6hsbdi2KfxwwWWVvlyz1DtRoDVrovRH_SdFz3ytEKRgogMrAjN-eI000usFRBCjsVt7Wn8aINgBFoSJm3mzbchdCtWvQ_mp3.mp3: 0 tracks in 4.96s   2025-12-30 13:27:54,044 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
Processing files: 100%|█████████████████████████████████████████████████████████████| 26/26 [01:09<00:00,  2.69s/it] 
2025-12-30 13:27:54,048 - engine.batch_runner - INFO - Processing batch_2: 2 files
2025-12-30 13:27:54,048 - engine.batch_runner - INFO -   🚀 Using GPU acceleration for batch
2025-12-30 13:27:54,048 - preprocessing.source_separator - INFO - Loading Demucs model 'htdemucs' on cpu...
2025-12-30 13:27:54,571 - preprocessing.source_separator - INFO - Demucs model loaded successfully
2025-12-30 13:27:54,572 - engine.batch_runner - INFO - Processing file: CHENNURU SHREYA REDDY-2512041909.wav
2025-12-30 13:27:54,573 - engine.batch_runner - INFO - Configuration validation passed
2025-12-30 13:27:54,573 - engine.batch_runner - INFO - Processing file: CHENNURU SHREYA REDDY-2512041909.mp3
2025-12-30 13:27:54,573 - engine.batch_runner - INFO - Configuration validation passed
Processing files:   0%|                                                                       | 0/2 [00:00<?, ?it/s]2
025-12-30 13:27:56,359 - engine.batch_runner - INFO - Separating vocals from accompaniment...                        2025-12-30 13:27:56,363 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:27:56,376 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:27:56,463 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:27:56,466 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:27:56,468 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:28:04,412 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:28:04,414 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:28:05,423 - engine.batch_runner - INFO - Successfully processed data/input\CHENNURU SHREYA REDDY-251204
1909.mp3: 0 tracks in 9.84s                                                                                          2025-12-30 13:28:05,424 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:28:05,423 - engine.batch_runner - INFO - Successfully processed data/input\CHENNURU SHREYA REDDY-251204
1909.wav: 0 tracks in 9.85s                                                                                          Processing files:  50%|███████████████████████████████▌                               | 1/2 [00:10<00:10, 10.85s/it]2
025-12-30 13:28:05,425 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}  Processing files: 100%|███████████████████████████████████████████████████████████████| 2/2 [00:10<00:00,  5.43s/it] 
2025-12-30 13:28:05,430 - engine.batch_runner - INFO - Processing batch_3: 2 files
2025-12-30 13:28:05,431 - engine.batch_runner - INFO -   🚀 Using GPU acceleration for batch
2025-12-30 13:28:05,431 - preprocessing.source_separator - INFO - Loading Demucs model 'htdemucs' on cpu...
2025-12-30 13:28:05,846 - preprocessing.source_separator - INFO - Demucs model loaded successfully
2025-12-30 13:28:05,848 - engine.batch_runner - INFO - Processing file: CHENNURU SHREYA REDDY-2512142242.wav
2025-12-30 13:28:05,849 - engine.batch_runner - INFO - Configuration validation passed
2025-12-30 13:28:05,849 - engine.batch_runner - INFO - Processing file: CHENNURU SHREYA REDDY-2512142242.mp3
2025-12-30 13:28:05,850 - engine.batch_runner - INFO - Configuration validation passed
Processing files:   0%|                                                                       | 0/2 [00:00<?, ?it/s]2
025-12-30 13:28:06,940 - engine.batch_runner - INFO - Separating vocals from accompaniment...                        2025-12-30 13:28:06,950 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:28:06,965 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:28:07,061 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:28:07,074 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:28:07,082 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:28:28,534 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:28:28,542 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:28:29,562 - engine.batch_runner - INFO - Successfully processed data/input\CHENNURU SHREYA REDDY-251214
2242.mp3: 0 tracks in 22.71s                                                                                         2025-12-30 13:28:29,562 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:28:29,567 - engine.batch_runner - INFO - Successfully processed data/input\CHENNURU SHREYA REDDY-251214
2242.wav: 0 tracks in 22.71s                                                                                         Processing files:  50%|███████████████████████████████▌                               | 1/2 [00:23<00:23, 23.72s/it]2
025-12-30 13:28:29,570 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}  Processing files: 100%|███████████████████████████████████████████████████████████████| 2/2 [00:23<00:00, 11.86s/it] 
2025-12-30 13:28:29,595 - preprocessing.source_separator - INFO - Loading Demucs model 'htdemucs' on cpu...
2025-12-30 13:28:30,197 - preprocessing.source_separator - INFO - Demucs model loaded successfully
2025-12-30 13:28:30,197 - preprocessing.source_separator - INFO - Loading Demucs model 'htdemucs' on cpu...
2025-12-30 13:28:31,123 - preprocessing.source_separator - INFO - Demucs model loaded successfully
2025-12-30 13:28:31,146 - engine.batch_runner - INFO - Processing file: CHENNURU SHREYA REDDY-2512041909.wav
2025-12-30 13:28:31,147 - engine.batch_runner - INFO - Configuration validation passed
2025-12-30 13:28:31,148 - engine.batch_runner - INFO - Processing file: CHENNURU SHREYA REDDY-2512041914.wav
2025-12-30 13:28:31,150 - engine.batch_runner - INFO - Configuration validation passed
Processing files:   0%|                                                                      | 0/30 [00:00<?, ?it/s]2
025-12-30 13:28:32,163 - engine.batch_runner - INFO - Separating vocals from accompaniment...                        2025-12-30 13:28:32,167 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:28:32,175 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:28:32,177 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:28:32,181 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:28:32,183 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:28:35,551 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:28:37,124 - engine.batch_runner - INFO - Successfully processed data/input\CHENNURU SHREYA REDDY-251204
1914.wav: 0 tracks in 4.45s                                                                                          2025-12-30 13:28:37,129 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:28:37,130 - engine.batch_runner - INFO - Processing file: CHENNURU SHREYA REDDY-2512041915.wav
Processing files:   3%|██                                                            | 1/30 [00:05<02:53,  5.98s/it]2
025-12-30 13:28:37,130 - engine.batch_runner - INFO - Configuration validation passed                                2025-12-30 13:28:37,636 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:28:38,148 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:28:38,149 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:28:38,152 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:28:38,948 - engine.batch_runner - INFO - Successfully processed data/input\CHENNURU SHREYA REDDY-251204
1909.wav: 0 tracks in 6.50s                                                                                          2025-12-30 13:28:38,965 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:28:38,982 - engine.batch_runner - INFO - Processing file: CHENNURU SHREYA REDDY-2512142242.wav
Processing files:   7%|████▏                                                         | 2/30 [00:07<01:39,  3.56s/it]2
025-12-30 13:28:39,042 - engine.batch_runner - INFO - Configuration validation passed                                2025-12-30 13:28:40,403 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:28:40,414 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:28:40,420 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:28:40,520 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:28:44,277 - engine.batch_runner - INFO - Successfully processed data/input\CHENNURU SHREYA REDDY-251204
1915.wav: 0 tracks in 3.39s                                                                                          2025-12-30 13:28:44,284 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:28:44,301 - engine.batch_runner - INFO - Processing file: CHENNURU SHREYA REDDY-2512142309.wav
2025-12-30 13:28:44,316 - engine.batch_runner - INFO - Configuration validation passed
Processing files:  10%|██████▏                                                       | 3/30 [00:13<01:57,  4.36s/it]2
025-12-30 13:28:45,610 - engine.batch_runner - INFO - Separating vocals from accompaniment...                        2025-12-30 13:28:45,688 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:28:45,736 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:28:49,321 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:28:50,325 - engine.batch_runner - INFO - Successfully processed data/input\CHENNURU SHREYA REDDY-251214
2309.wav: 0 tracks in 5.02s                                                                                          2025-12-30 13:28:50,326 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:28:50,327 - engine.batch_runner - INFO - Processing file: CHENNURU SHREYA REDDY-2512142317.wav
Processing files:  13%|████████▎                                                     | 4/30 [00:19<02:10,  5.01s/it]2
025-12-30 13:28:50,327 - engine.batch_runner - INFO - Configuration validation passed                                2025-12-30 13:28:51,456 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:28:51,469 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:28:51,470 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:28:53,541 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:28:54,202 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:28:54,545 - engine.batch_runner - INFO - Successfully processed data/input\CHENNURU SHREYA REDDY-251214
2317.wav: 0 tracks in 3.22s                                                                                          2025-12-30 13:28:54,545 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:28:54,546 - engine.batch_runner - INFO - Processing file: CHENNURU SHREYA REDDY-2512142319.wav
Processing files:  17%|██████████▎                                                   | 5/30 [00:23<01:58,  4.73s/it]2
025-12-30 13:28:54,546 - engine.batch_runner - INFO - Configuration validation passed                                2025-12-30 13:28:55,215 - engine.batch_runner - INFO - Successfully processed data/input\CHENNURU SHREYA REDDY-251214
2242.wav: 0 tracks in 15.23s                                                                                         2025-12-30 13:28:55,215 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:28:55,220 - engine.batch_runner - INFO - Processing file: SaveClip.App_AQMGdlsfbIp7x2NXYZ8wKYDI4cJebCC1
am_SlMX33HZV2bFNDV-teg2M0n-PoCDozUg8TwjqdLzYfeN2ei9gB4NFznFPuoa1Mx7V8GU_mp3.wav                                      Processing files:  20%|████████████▍                                                 | 6/30 [00:24<01:20,  3.35s/it]2
025-12-30 13:28:55,220 - engine.batch_runner - INFO - Configuration validation passed                                2025-12-30 13:28:55,560 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:28:55,561 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:28:55,562 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:28:56,235 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:28:56,329 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:28:56,377 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:28:57,977 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:28:58,004 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:28:58,980 - engine.batch_runner - INFO - Successfully processed data/input\SaveClip.App_AQMGdlsfbIp7x2N
XYZ8wKYDI4cJebCC1am_SlMX33HZV2bFNDV-teg2M0n-PoCDozUg8TwjqdLzYfeN2ei9gB4NFznFPuoa1Mx7V8GU_mp3.wav: 0 tracks in 2.76s  2025-12-30 13:28:58,980 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:28:58,981 - engine.batch_runner - INFO - Processing file: SaveClip.App_AQNGxC8bWFDBf_Iz3MoSshZCuOHDVF_4
M3Cta9NVxuDWRfhUDpKo51cdv7zk1INEiU8jwjV_mj23zg7n7WWatiDzew9jh57Cnr7K7FE_mp3.wav                                      Processing files:  23%|██████████████▍                                               | 7/30 [00:27<01:20,  3.48s/it]2
025-12-30 13:28:58,981 - engine.batch_runner - INFO - Configuration validation passed                                2025-12-30 13:28:59,008 - engine.batch_runner - INFO - Successfully processed data/input\CHENNURU SHREYA REDDY-251214
2319.wav: 0 tracks in 3.46s                                                                                          2025-12-30 13:28:59,008 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0} 
2025-12-30 13:28:59,009 - engine.batch_runner - INFO - Processing file: SaveClip.App_AQNY-VBXQ0HoJbbRNj5uJ5BGv5CnBh0S
fBBa-SqO2tXSSbq2u5soG4FUnBHyMy79T6P7hOqFzYgZ3KA6Q7MTI9euBK4PbHsEBmYJrNg_mp3.wav                                      2025-12-30 13:28:59,009 - engine.batch_runner - INFO - Configuration validation passed
2025-12-30 13:28:59,989 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:28:59,990 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:28:59,992 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:29:00,020 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:29:00,023 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:29:00,027 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:29:02,555 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:29:02,604 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:29:03,558 - engine.batch_runner - INFO - Successfully processed data/input\SaveClip.App_AQNGxC8bWFDBf_I
z3MoSshZCuOHDVF_4M3Cta9NVxuDWRfhUDpKo51cdv7zk1INEiU8jwjV_mj23zg7n7WWatiDzew9jh57Cnr7K7FE_mp3.wav: 0 tracks in 3.58s  2025-12-30 13:29:03,558 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:29:03,558 - engine.batch_runner - INFO - Processing file: SaveClip.App_AQOtF76z2pcjZsJ81Weobl6mUyRogrBB
oISDTV4Ut9FCG2ar3O5WTcnHBEnI2_W5cdMEl9gbCmWQKap0Yb_Y0fKm6hMIdgjIPyp7v0A_mp3.wav                                      Processing files:  30%|██████████████████▌                                           | 9/30 [00:32<01:01,  2.91s/it]2
025-12-30 13:29:03,559 - engine.batch_runner - INFO - Configuration validation passed                                2025-12-30 13:29:03,607 - engine.batch_runner - INFO - Successfully processed data/input\SaveClip.App_AQNY-VBXQ0HoJbb
RNj5uJ5BGv5CnBh0SfBBa-SqO2tXSSbq2u5soG4FUnBHyMy79T6P7hOqFzYgZ3KA6Q7MTI9euBK4PbHsEBmYJrNg_mp3.wav: 0 tracks in 3.60s  2025-12-30 13:29:03,607 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:29:03,608 - engine.batch_runner - INFO - Processing file: SaveClip.App_AQPE6zNGrNOfgNmsSazKS7aKZWM7orc4
x_kL0p8DNnLzkYGXVHjhIBUizMjtN1toOQVZyaZhA8cDsfoPI8_cvCkn5wSHmE44U0UOusY_mp3.wav                                      2025-12-30 13:29:03,608 - engine.batch_runner - INFO - Configuration validation passed
2025-12-30 13:29:04,570 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:29:04,571 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:29:04,574 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:29:04,616 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:29:04,619 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:29:04,620 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:29:07,677 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:29:07,823 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:29:08,681 - engine.batch_runner - INFO - Successfully processed data/input\SaveClip.App_AQPE6zNGrNOfgNm
sSazKS7aKZWM7orc4x_kL0p8DNnLzkYGXVHjhIBUizMjtN1toOQVZyaZhA8cDsfoPI8_cvCkn5wSHmE44U0UOusY_mp3.wav: 0 tracks in 4.07s  2025-12-30 13:29:08,681 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:29:08,682 - engine.batch_runner - INFO - Processing file: SaveClip.App_AQPHd0BpHWrZQx5SPV3IqsOYRXFnPSg0
uOWNG_fTqqbZAhekmA-hiPztX05TscDCldBU4VpHsxxmllpXY1ovIVV51m2oPyNtOoA5Ns4_mp3.wav                                      Processing files:  37%|██████████████████████▎                                      | 11/30 [00:37<00:52,  2.77s/it]2
025-12-30 13:29:08,682 - engine.batch_runner - INFO - Configuration validation passed                                2025-12-30 13:29:08,826 - engine.batch_runner - INFO - Successfully processed data/input\SaveClip.App_AQOtF76z2pcjZsJ
81Weobl6mUyRogrBBoISDTV4Ut9FCG2ar3O5WTcnHBEnI2_W5cdMEl9gbCmWQKap0Yb_Y0fKm6hMIdgjIPyp7v0A_mp3.wav: 0 tracks in 4.27s  2025-12-30 13:29:08,826 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:29:08,827 - engine.batch_runner - INFO - Processing file: SaveClip.App_AQPIygeuh5zlcgu5a1zl_QZWcZkPkGh4
6_T6y9Suuzg3PMaBa8sDX74vM7BqgGr5URYCULlvW71oE8MZBSpl_TaUgsYDdWAgni940nM_mp3.wav                                      Processing files:  40%|████████████████████████▍                                    | 12/30 [00:37<00:39,  2.17s/it]2
025-12-30 13:29:08,827 - engine.batch_runner - INFO - Configuration validation passed                                2025-12-30 13:29:09,691 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:29:09,692 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:29:09,694 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:29:10,350 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:29:10,434 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:29:10,481 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:29:12,766 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:29:12,841 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:29:13,770 - engine.batch_runner - INFO - Successfully processed data/input\SaveClip.App_AQPIygeuh5zlcgu
5a1zl_QZWcZkPkGh46_T6y9Suuzg3PMaBa8sDX74vM7BqgGr5URYCULlvW71oE8MZBSpl_TaUgsYDdWAgni940nM_mp3.wav: 0 tracks in 3.94s  2025-12-30 13:29:13,770 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:29:13,771 - engine.batch_runner - INFO - Processing file: SaveClip.App_AQPlyxJuQuh6hsbdi2KfxwwWWVvlyz1D
tRoDVrovRH_SdFz3ytEKRgogMrAjN-eI000usFRBCjsVt7Wn8aINgBFoSJm3mzbchdCtWvQ_mp3.wav                                      Processing files:  43%|██████████████████████████▍                                  | 13/30 [00:42<00:48,  2.85s/it]2
025-12-30 13:29:13,771 - engine.batch_runner - INFO - Configuration validation passed                                2025-12-30 13:29:13,845 - engine.batch_runner - INFO - Successfully processed data/input\SaveClip.App_AQPHd0BpHWrZQx5
SPV3IqsOYRXFnPSg0uOWNG_fTqqbZAhekmA-hiPztX05TscDCldBU4VpHsxxmllpXY1ovIVV51m2oPyNtOoA5Ns4_mp3.wav: 0 tracks in 4.16s  2025-12-30 13:29:13,845 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:29:13,846 - engine.batch_runner - INFO - Processing file: CHENNURU SHREYA REDDY-2512041909.mp3
2025-12-30 13:29:13,846 - engine.batch_runner - INFO - Configuration validation passed
2025-12-30 13:29:15,043 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:29:15,045 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:29:15,047 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:29:15,093 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:29:15,097 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:29:15,099 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:29:21,245 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:29:22,249 - engine.batch_runner - INFO - Successfully processed data/input\SaveClip.App_AQPlyxJuQuh6hsb
di2KfxwwWWVvlyz1DtRoDVrovRH_SdFz3ytEKRgogMrAjN-eI000usFRBCjsVt7Wn8aINgBFoSJm3mzbchdCtWvQ_mp3.wav: 0 tracks in 7.48s  2025-12-30 13:29:22,249 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:29:22,250 - engine.batch_runner - INFO - Processing file: CHENNURU SHREYA REDDY-2512041914.mp3
Processing files:  50%|██████████████████████████████▌                              | 15/30 [00:51<00:51,  3.42s/it]2
025-12-30 13:29:22,250 - engine.batch_runner - INFO - Configuration validation passed                                2025-12-30 13:29:22,331 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:29:23,336 - engine.batch_runner - INFO - Successfully processed data/input\CHENNURU SHREYA REDDY-251204
1909.mp3: 0 tracks in 8.49s                                                                                          2025-12-30 13:29:23,337 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:29:23,338 - engine.batch_runner - INFO - Processing file: CHENNURU SHREYA REDDY-2512041915.mp3
Processing files:  53%|████████████████████████████████▌                            | 16/30 [00:52<00:40,  2.89s/it]2
025-12-30 13:29:23,338 - engine.batch_runner - INFO - Configuration validation passed                                2025-12-30 13:29:23,405 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:29:23,407 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:29:23,409 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:29:24,673 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:29:24,783 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:29:24,785 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:29:24,786 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:29:25,688 - engine.batch_runner - INFO - Successfully processed data/input\CHENNURU SHREYA REDDY-251204
1914.mp3: 0 tracks in 2.42s                                                                                          2025-12-30 13:29:25,704 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:29:25,720 - engine.batch_runner - INFO - Processing file: CHENNURU SHREYA REDDY-2512142242.mp3
2025-12-30 13:29:25,736 - engine.batch_runner - INFO - Configuration validation passed
Processing files:  57%|██████████████████████████████████▌                          | 17/30 [00:54<00:36,  2.77s/it]2
025-12-30 13:29:27,234 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'                  2025-12-30 13:29:27,429 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:29:27,437 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:29:27,447 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:29:31,274 - engine.batch_runner - INFO - Successfully processed data/input\CHENNURU SHREYA REDDY-251204
1915.mp3: 0 tracks in 3.90s                                                                                          2025-12-30 13:29:31,289 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:29:31,306 - engine.batch_runner - INFO - Processing file: CHENNURU SHREYA REDDY-2512142309.mp3
2025-12-30 13:29:31,321 - engine.batch_runner - INFO - Configuration validation passed
Processing files:  60%|████████████████████████████████████▌                        | 18/30 [01:00<00:41,  3.50s/it]2
025-12-30 13:29:32,771 - engine.batch_runner - INFO - Separating vocals from accompaniment...                        2025-12-30 13:29:32,865 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:29:32,912 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:29:36,484 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:29:37,487 - engine.batch_runner - INFO - Successfully processed data/input\CHENNURU SHREYA REDDY-251214
2309.mp3: 0 tracks in 5.18s                                                                                          2025-12-30 13:29:37,487 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:29:37,488 - engine.batch_runner - INFO - Processing file: CHENNURU SHREYA REDDY-2512142317.mp3
Processing files:  63%|██████████████████████████████████████▋                      | 19/30 [01:06<00:46,  4.22s/it]2
025-12-30 13:29:37,488 - engine.batch_runner - INFO - Configuration validation passed                                2025-12-30 13:29:38,527 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:29:38,528 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:29:38,530 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:29:40,888 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:29:41,034 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:29:41,892 - engine.batch_runner - INFO - Successfully processed data/input\CHENNURU SHREYA REDDY-251214
2317.mp3: 0 tracks in 3.40s                                                                                          2025-12-30 13:29:41,892 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:29:41,893 - engine.batch_runner - INFO - Processing file: CHENNURU SHREYA REDDY-2512142319.mp3
Processing files:  67%|████████████████████████████████████████▋                    | 20/30 [01:10<00:42,  4.27s/it]2
025-12-30 13:29:41,893 - engine.batch_runner - INFO - Configuration validation passed                                2025-12-30 13:29:42,051 - engine.batch_runner - INFO - Successfully processed data/input\CHENNURU SHREYA REDDY-251214
2242.mp3: 0 tracks in 15.33s                                                                                         2025-12-30 13:29:42,051 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:29:42,056 - engine.batch_runner - INFO - Processing file: SaveClip.App_AQMGdlsfbIp7x2NXYZ8wKYDI4cJebCC1
am_SlMX33HZV2bFNDV-teg2M0n-PoCDozUg8TwjqdLzYfeN2ei9gB4NFznFPuoa1Mx7V8GU_mp3.mp3                                      Processing files:  70%|██████████████████████████████████████████▋                  | 21/30 [01:10<00:27,  3.10s/it]2
025-12-30 13:29:42,056 - engine.batch_runner - INFO - Configuration validation passed                                2025-12-30 13:29:42,915 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:29:42,916 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:29:42,916 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:29:43,395 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:29:43,477 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:29:43,524 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:29:45,252 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:29:45,285 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:29:46,254 - engine.batch_runner - INFO - Successfully processed data/input\CHENNURU SHREYA REDDY-251214
2319.mp3: 0 tracks in 3.36s                                                                                          2025-12-30 13:29:46,254 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:29:46,256 - engine.batch_runner - INFO - Processing file: SaveClip.App_AQNGxC8bWFDBf_Iz3MoSshZCuOHDVF_4
M3Cta9NVxuDWRfhUDpKo51cdv7zk1INEiU8jwjV_mj23zg7n7WWatiDzew9jh57Cnr7K7FE_mp3.mp3                                      Processing files:  73%|████████████████████████████████████████████▋                | 22/30 [01:15<00:27,  3.42s/it]2
025-12-30 13:29:46,256 - engine.batch_runner - INFO - Configuration validation passed                                2025-12-30 13:29:46,287 - engine.batch_runner - INFO - Successfully processed data/input\SaveClip.App_AQMGdlsfbIp7x2N
XYZ8wKYDI4cJebCC1am_SlMX33HZV2bFNDV-teg2M0n-PoCDozUg8TwjqdLzYfeN2ei9gB4NFznFPuoa1Mx7V8GU_mp3.mp3: 0 tracks in 3.23s  2025-12-30 13:29:46,287 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:29:46,288 - engine.batch_runner - INFO - Processing file: SaveClip.App_AQNY-VBXQ0HoJbbRNj5uJ5BGv5CnBh0S
fBBa-SqO2tXSSbq2u5soG4FUnBHyMy79T6P7hOqFzYgZ3KA6Q7MTI9euBK4PbHsEBmYJrNg_mp3.mp3                                      2025-12-30 13:29:46,288 - engine.batch_runner - INFO - Configuration validation passed
2025-12-30 13:29:47,307 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:29:47,308 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:29:47,309 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:29:47,338 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:29:47,341 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:29:47,342 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:29:49,850 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:29:49,912 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:29:50,854 - engine.batch_runner - INFO - Successfully processed data/input\SaveClip.App_AQNGxC8bWFDBf_I
z3MoSshZCuOHDVF_4M3Cta9NVxuDWRfhUDpKo51cdv7zk1INEiU8jwjV_mj23zg7n7WWatiDzew9jh57Cnr7K7FE_mp3.mp3: 0 tracks in 3.60s  2025-12-30 13:29:50,854 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:29:50,855 - engine.batch_runner - INFO - Processing file: SaveClip.App_AQOtF76z2pcjZsJ81Weobl6mUyRogrBB
oISDTV4Ut9FCG2ar3O5WTcnHBEnI2_W5cdMEl9gbCmWQKap0Yb_Y0fKm6hMIdgjIPyp7v0A_mp3.mp3                                      Processing files:  80%|████████████████████████████████████████████████▊            | 24/30 [01:19<00:17,  2.91s/it]2
025-12-30 13:29:50,855 - engine.batch_runner - INFO - Configuration validation passed                                2025-12-30 13:29:50,916 - engine.batch_runner - INFO - Successfully processed data/input\SaveClip.App_AQNY-VBXQ0HoJbb
RNj5uJ5BGv5CnBh0SfBBa-SqO2tXSSbq2u5soG4FUnBHyMy79T6P7hOqFzYgZ3KA6Q7MTI9euBK4PbHsEBmYJrNg_mp3.mp3: 0 tracks in 3.63s  2025-12-30 13:29:50,916 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:29:50,917 - engine.batch_runner - INFO - Processing file: SaveClip.App_AQPE6zNGrNOfgNmsSazKS7aKZWM7orc4
x_kL0p8DNnLzkYGXVHjhIBUizMjtN1toOQVZyaZhA8cDsfoPI8_cvCkn5wSHmE44U0UOusY_mp3.mp3                                      2025-12-30 13:29:50,917 - engine.batch_runner - INFO - Configuration validation passed
2025-12-30 13:29:51,915 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:29:51,917 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:29:51,918 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:29:51,965 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:29:51,967 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:29:51,968 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:29:54,970 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:29:55,115 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:29:55,972 - engine.batch_runner - INFO - Successfully processed data/input\SaveClip.App_AQPE6zNGrNOfgNm
sSazKS7aKZWM7orc4x_kL0p8DNnLzkYGXVHjhIBUizMjtN1toOQVZyaZhA8cDsfoPI8_cvCkn5wSHmE44U0UOusY_mp3.mp3: 0 tracks in 4.05s  2025-12-30 13:29:55,972 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:29:55,973 - engine.batch_runner - INFO - Processing file: SaveClip.App_AQPHd0BpHWrZQx5SPV3IqsOYRXFnPSg0
uOWNG_fTqqbZAhekmA-hiPztX05TscDCldBU4VpHsxxmllpXY1ovIVV51m2oPyNtOoA5Ns4_mp3.mp3                                      Processing files:  87%|████████████████████████████████████████████████████▊        | 26/30 [01:24<00:11,  2.77s/it]2
025-12-30 13:29:55,974 - engine.batch_runner - INFO - Configuration validation passed                                2025-12-30 13:29:56,118 - engine.batch_runner - INFO - Successfully processed data/input\SaveClip.App_AQOtF76z2pcjZsJ
81Weobl6mUyRogrBBoISDTV4Ut9FCG2ar3O5WTcnHBEnI2_W5cdMEl9gbCmWQKap0Yb_Y0fKm6hMIdgjIPyp7v0A_mp3.mp3: 0 tracks in 4.26s  2025-12-30 13:29:56,118 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:29:56,119 - engine.batch_runner - INFO - Processing file: SaveClip.App_AQPIygeuh5zlcgu5a1zl_QZWcZkPkGh4
6_T6y9Suuzg3PMaBa8sDX74vM7BqgGr5URYCULlvW71oE8MZBSpl_TaUgsYDdWAgni940nM_mp3.mp3                                      2025-12-30 13:29:56,119 - engine.batch_runner - INFO - Configuration validation passed
Processing files:  90%|██████████████████████████████████████████████████████▉      | 27/30 [01:24<00:06,  2.20s/it]2
025-12-30 13:29:57,017 - engine.batch_runner - INFO - Separating vocals from accompaniment...                        2025-12-30 13:29:57,018 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:29:57,020 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:29:57,628 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:29:57,716 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:29:57,764 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:29:59,868 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:29:59,915 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:30:00,871 - engine.batch_runner - INFO - Successfully processed data/input\SaveClip.App_AQPIygeuh5zlcgu
5a1zl_QZWcZkPkGh46_T6y9Suuzg3PMaBa8sDX74vM7BqgGr5URYCULlvW71oE8MZBSpl_TaUgsYDdWAgni940nM_mp3.mp3: 0 tracks in 3.75s  2025-12-30 13:30:00,871 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:30:00,871 - engine.batch_runner - INFO - Processing file: SaveClip.App_AQPlyxJuQuh6hsbdi2KfxwwWWVvlyz1D
tRoDVrovRH_SdFz3ytEKRgogMrAjN-eI000usFRBCjsVt7Wn8aINgBFoSJm3mzbchdCtWvQ_mp3.mp3                                      Processing files:  93%|████████████████████████████████████████████████████████▉    | 28/30 [01:29<00:05,  2.81s/it]2
025-12-30 13:30:00,872 - engine.batch_runner - INFO - Configuration validation passed                                2025-12-30 13:30:00,919 - engine.batch_runner - INFO - Successfully processed data/input\SaveClip.App_AQPHd0BpHWrZQx5
SPV3IqsOYRXFnPSg0uOWNG_fTqqbZAhekmA-hiPztX05TscDCldBU4VpHsxxmllpXY1ovIVV51m2oPyNtOoA5Ns4_mp3.mp3: 0 tracks in 3.94s  2025-12-30 13:30:00,919 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
2025-12-30 13:30:01,941 - engine.batch_runner - INFO - Separating vocals from accompaniment...
2025-12-30 13:30:01,944 - preprocessing.source_separator - ERROR - Error during vocal separation: convert_audio() got
 an unexpected keyword argument 'channels_first'                                                                     2025-12-30 13:30:01,946 - engine.batch_runner - INFO - Classifying separated vocal track...
2025-12-30 13:30:04,045 - engine.batch_runner - ERROR - Error classifying vocal track: 'sample_rate'
2025-12-30 13:30:05,048 - engine.batch_runner - INFO - Successfully processed data/input\SaveClip.App_AQPlyxJuQuh6hsb
di2KfxwwWWVvlyz1DtRoDVrovRH_SdFz3ytEKRgogMrAjN-eI000usFRBCjsVt7Wn8aINgBFoSJm3mzbchdCtWvQ_mp3.mp3: 0 tracks in 3.18s  2025-12-30 13:30:05,048 - engine.batch_runner - INFO - Gender distribution: {'male': 0, 'female': 0, 'uncertain': 0}
Processing files: 100%|█████████████████████████████████████████████████████████████| 30/30 [01:33<00:00,  3.13s/it] 
2025-12-30 13:30:05,091 - engine.batch_runner - INFO - Batch processing completed: 30 successful, 0 failed

✅ Pipeline completed in 210.04 seconds

Results summary:
  status: completed
  total_files: 30
  successful: 30
  failed: 0
  results: [{'file': 'CHENNURU SHREYA REDDY-2512041914.wav', 'segments_processed': 0, 'gender_distribution': {'male':
 0, 'female': 0, 'uncertain': 0}, 'processing_time': 4.4489426612854, 'memory_delta': 0.0876617431640625}, {'file': 'CHENNURU SHREYA REDDY-2512041909.wav', 'segments_processed': 0, 'gender_distribution': {'male': 0, 'female': 0, 'uncertain': 0}, 'processing_time': 6.495448350906372, 'memory_delta': -0.05216217041015625}, {'file': 'CHENNURU SHREYA REDDY-2512041915.wav', 'segments_processed': 0, 'gender_distribution': {'male': 0, 'female': 0, 'uncertain': 0}, 'processing_time': 3.3936314582824707, 'memory_delta': -0.024448394775390625}, {'file': 'CHENNURU SHREYA REDDY-2512142309.wav', 'segments_processed': 0, 'gender_distribution': {'male': 0, 'female': 0, 'uncertain': 0}, 'processing_time': 5.022742986679077, 'memory_delta': 0.0456085205078125}, {'file': 'CHENNURU SHREYA REDDY-2512142317.wav', 'segments_processed': 0, 'gender_distribution': {'male': 0, 'female': 0, 'uncertain': 0}, 'processing_time': 3.217409610748291, 'memory_delta': -0.2625999450683594}, {'file': 'CHENNURU SHREYA REDDY-2512142242.wav', 'segments_processed': 0, 'gender_distribution': {'male': 0, 'female': 0, 'uncertain': 0}, 'processing_time': 15.231872797012329, 'memory_delta': -0.2589836120605469}, {'file': 'SaveClip.App_AQMGdlsfbIp7x2NXYZ8wKYDI4cJebCC1am_SlMX33HZV2bFNDV-teg2M0n-PoCDozUg8TwjqdLzYfeN2ei9gB4NFznFPuoa1Mx7V8GU_mp3.wav', 'segments_processed': 0, 'gender_distribution': {'male': 0, 'female': 0, 'uncertain': 0}, 'processing_time': 2.75834059715271, 'memory_delta': -0.048114776611328125}, {'file': 'CHENNURU SHREYA REDDY-2512142319.wav', 'segments_processed': 0, 'gender_distribution': {'male': 0, 'female': 0, 'uncertain': 0}, 'processing_time': 3.461040496826172, 'memory_delta': -0.11081695556640625}, {'file': 'SaveClip.App_AQNGxC8bWFDBf_Iz3MoSshZCuOHDVF_4M3Cta9NVxuDWRfhUDpKo51cdv7zk1INEiU8jwjV_mj23zg7n7WWatiDzew9jh57Cnr7K7FE_mp3.wav', 'segments_processed': 0, 'gender_distribution': {'male': 0, 'female': 0, 'uncertain': 0}, 'processing_time': 3.57543683052063, 'memory_delta': 0.055942535400390625}, {'file': 'SaveClip.App_AQNY-VBXQ0HoJbbRNj5uJ5BGv5CnBh0SfBBa-SqO2tXSSbq2u5soG4FUnBHyMy79T6P7hOqFzYgZ3KA6Q7MTI9euBK4PbHsEBmYJrNg_mp3.wav', 'segments_processed': 0, 'gender_distribution': {'male': 0, 'female': 0, 'uncertain': 0}, 'processing_time': 3.5960609912872314, 'memory_delta': 0.040454864501953125}, {'file': 'SaveClip.App_AQPE6zNGrNOfgNmsSazKS7aKZWM7orc4x_kL0p8DNnLzkYGXVHjhIBUizMjtN1toOQVZyaZhA8cDsfoPI8_cvCkn5wSHmE44U0UOusY_mp3.wav', 'segments_processed': 0, 'gender_distribution': {'male': 0, 'female': 0, 'uncertain': 0}, 'processing_time': 4.071655035018921, 'memory_delta': 0.06996917724609375}, {'file': 'SaveClip.App_AQOtF76z2pcjZsJ81Weobl6mUyRogrBBoISDTV4Ut9FCG2ar3O5WTcnHBEnI2_W5cdMEl9gbCmWQKap0Yb_Y0fKm6hMIdgjIPyp7v0A_mp3.wav', 'segments_processed': 0, 'gender_distribution': {'male': 0, 'female': 0, 'uncertain': 0}, 'processing_time': 4.2675158977508545, 'memory_delta': 0.06344985961914062}, {'file': 'SaveClip.App_AQPIygeuh5zlcgu5a1zl_QZWcZkPkGh46_T6y9Suuzg3PMaBa8sDX74vM7BqgGr5URYCULlvW71oE8MZBSpl_TaUgsYDdWAgni940nM_mp3.wav', 'segments_processed': 0, 'gender_distribution': {'male': 0, 'female': 0, 'uncertain': 0}, 'processing_time': 3.9403107166290283, 'memory_delta': 0.2714958190917969}, {'file': 'SaveClip.App_AQPHd0BpHWrZQx5SPV3IqsOYRXFnPSg0uOWNG_fTqqbZAhekmA-hiPztX05TscDCldBU4VpHsxxmllpXY1ovIVV51m2oPyNtOoA5Ns4_mp3.wav', 'segments_processed': 0, 'gender_distribution': {'male': 0, 'female': 0, 'uncertain': 0}, 'processing_time': 4.163153171539307, 'memory_delta': 0.26570892333984375}, {'file': 'SaveClip.App_AQPlyxJuQuh6hsbdi2KfxwwWWVvlyz1DtRoDVrovRH_SdFz3ytEKRgogMrAjN-eI000usFRBCjsVt7Wn8aINgBFoSJm3mzbchdCtWvQ_mp3.wav', 'segments_processed': 0, 'gender_distribution': {'male': 0, 'female': 0, 'uncertain': 0}, 'processing_time': 7.476986646652222, 'memory_delta': -0.051532745361328125}, {'file': 'CHENNURU SHREYA REDDY-2512041909.mp3', 'segments_processed': 0, 'gender_distribution': {'male': 0, 'female': 0, 'uncertain': 0}, 'processing_time': 8.488465309143066, 'memory_delta': -0.20151138305664062}, {'file': 'CHENNURU SHREYA REDDY-2512041914.mp3', 'segments_processed': 0, 'gender_distribution': {'male': 0, 'female': 0, 'uncertain': 0}, 'processing_time': 2.4247846603393555, 'memory_delta': -0.17266845703125}, {'file': 'CHENNURU SHREYA REDDY-2512041915.mp3', 'segments_processed': 0, 'gender_distribution': {'male': 0, 'female': 0, 'uncertain': 0}, 'processing_time': 3.8993706703186035, 'memory_delta': -0.03897857666015625}, {'file': 'CHENNURU SHREYA REDDY-2512142309.mp3', 'segments_processed': 0, 'gender_distribution': {'male': 0, 'female': 0, 'uncertain': 0}, 'processing_time': 5.179967403411865, 'memory_delta': 0.1536712646484375}, {'file': 'CHENNURU SHREYA REDDY-2512142317.mp3', 'segments_processed': 0, 'gender_distribution': {'male': 0, 'female': 0, 'uncertain': 0}, 'processing_time': 3.402799606323242, 'memory_delta': -0.2565155029296875}, {'file': 'CHENNURU SHREYA REDDY-2512142242.mp3', 'segments_processed': 0, 'gender_distribution': {'male': 0, 'female': 0, 'uncertain': 0}, 'processing_time': 15.328909158706665, 'memory_delta': -0.07683181762695312}, {'file': 'CHENNURU SHREYA REDDY-2512142319.mp3', 'segments_processed': 0, 'gender_distribution': {'male': 0, 'female': 0, 'uncertain': 0}, 'processing_time': 3.360267400741577, 'memory_delta': 0.035640716552734375}, {'file': 'SaveClip.App_AQMGdlsfbIp7x2NXYZ8wKYDI4cJebCC1am_SlMX33HZV2bFNDV-teg2M0n-PoCDozUg8TwjqdLzYfeN2ei9gB4NFznFPuoa1Mx7V8GU_mp3.mp3', 'segments_processed': 0, 'gender_distribution': {'male': 0, 'female': 0, 'uncertain': 0}, 'processing_time': 3.2296652793884277, 'memory_delta': 0.069366455078125}, {'file': 'SaveClip.App_AQNGxC8bWFDBf_Iz3MoSshZCuOHDVF_4M3Cta9NVxuDWRfhUDpKo51cdv7zk1INEiU8jwjV_mj23zg7n7WWatiDzew9jh57Cnr7K7FE_mp3.mp3', 'segments_processed': 0, 'gender_distribution': {'male': 0, 'female': 0, 'uncertain': 0}, 'processing_time': 3.5967061519622803, 'memory_delta': 0.062412261962890625}, {'file': 'SaveClip.App_AQNY-VBXQ0HoJbbRNj5uJ5BGv5CnBh0SfBBa-SqO2tXSSbq2u5soG4FUnBHyMy79T6P7hOqFzYgZ3KA6Q7MTI9euBK4PbHsEBmYJrNg_mp3.mp3', 'segments_processed': 0, 'gender_distribution': {'male': 0, 'female': 0, 'uncertain': 0}, 'processing_time': 3.6259734630584717, 'memory_delta': 0.02519989013671875}, {'file': 'SaveClip.App_AQPE6zNGrNOfgNmsSazKS7aKZWM7orc4x_kL0p8DNnLzkYGXVHjhIBUizMjtN1toOQVZyaZhA8cDsfoPI8_cvCkn5wSHmE44U0UOusY_mp3.mp3', 'segments_processed': 0, 'gender_distribution': {'male': 0, 'female': 0, 'uncertain': 0}, 'processing_time': 4.054325580596924, 'memory_delta': -0.10632705688476562}, {'file': 'SaveClip.App_AQOtF76z2pcjZsJ81Weobl6mUyRogrBBoISDTV4Ut9FCG2ar3O5WTcnHBEnI2_W5cdMEl9gbCmWQKap0Yb_Y0fKm6hMIdgjIPyp7v0A_mp3.mp3', 'segments_processed': 0, 'gender_distribution': {'male': 0, 'female': 0, 'uncertain': 0}, 'processing_time': 4.262470960617065, 'memory_delta': -0.1214447021484375}, {'file': 'SaveClip.App_AQPIygeuh5zlcgu5a1zl_QZWcZkPkGh46_T6y9Suuzg3PMaBa8sDX74vM7BqgGr5URYCULlvW71oE8MZBSpl_TaUgsYDdWAgni940nM_mp3.mp3', 'segments_processed': 0, 'gender_distribution': {'male': 0, 'female': 0, 'uncertain': 0}, 'processing_time': 3.7501060962677, 'memory_delta': 0.0662078857421875}, {'file': 'SaveClip.App_AQPHd0BpHWrZQx5SPV3IqsOYRXFnPSg0uOWNG_fTqqbZAhekmA-hiPztX05TscDCldBU4VpHsxxmllpXY1ovIVV51m2oPyNtOoA5Ns4_mp3.mp3', 'segments_processed': 0, 'gender_distribution': {'male': 0, 'female': 0, 'uncertain': 0}, 'processing_time': 3.9444260597229004, 'memory_delta': 0.0340576171875}, {'file': 'SaveClip.App_AQPlyxJuQuh6hsbdi2KfxwwWWVvlyz1DtRoDVrovRH_SdFz3ytEKRgogMrAjN-eI000usFRBCjsVt7Wn8aINgBFoSJm3mzbchdCtWvQ_mp3.mp3', 'segments_processed': 0, 'gender_distribution': {'male': 0, 'female': 0, 'uncertain': 0}, 'processing_time': 3.175891399383545, 'memory_delta': -0.000637054443359375}]                                                                            
====================================================================================================
  CHECKING OUTPUT DATA
====================================================================================================

  ✅ male/: 0 files
  ✅ female/: 76 files
  ✅ uncertain/: 0 files
  ⚠️  metadata.csv: not created

  Total samples: 76

====================================================================================================
  FINAL TEST REPORT
====================================================================================================


SUMMARY:
  dependencies: ✅ OK
  configuration: ✅ OK
  input_data: ✅ OK
  classifiers: ✅ OK
  pipeline: ✅ OK
  output_data: ✅ OK

====================================================================================================
  TEST EXECUTION COMPLETE
====================================================================================================


╔==================================================================================================╗
║                            ✅ ALL TESTS PASSED - VOXENT IS OPERATIONAL                            ║
╚==================================================================================================╝
