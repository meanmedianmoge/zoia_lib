using System;
using System.IO;
using System.Text;

namespace ZoiaFormatInterpreterTest
{
    class Program
    {
        static void Main(string[] args)
        {
            string filename = "";
            if (args.Length > 0)
            {
                filename = args[0];
            }
            FileStream fs = new FileStream(filename, FileMode.Open);
            
            byte[] bytes = new byte[4];            
            fs.Read(bytes, 0, 4);
            int presetSize = BitConverter.ToInt32(bytes, 0);
            Console.WriteLine(String.Format("Preset size = {0}", presetSize));

            bytes = new byte[16];
            fs.Read(bytes, 0, 16);
            string presetName = Encoding.UTF8.GetString(bytes, 0, bytes.Length);
            Console.WriteLine(String.Format("Patch name = {0}", presetName));

            bytes = new byte[4];
            fs.Read(bytes, 0, 4);
            int numberOfModules = BitConverter.ToInt32(bytes, 0);
            Console.WriteLine(String.Format("Module count = {0}", numberOfModules));

            for (int moduleNumber = 0; moduleNumber < numberOfModules; moduleNumber++)
            {
                Console.WriteLine(String.Format("Module #{0}", moduleNumber));
                bytes = new byte[4];
                fs.Read(bytes, 0, 4);
                int moduleSize = BitConverter.ToInt32(bytes, 0);

                int moduleSizeBytes = (moduleSize - 1) * 4;
                bytes = new byte[moduleSizeBytes];
                fs.Read(bytes, 0, moduleSizeBytes);

                int moduleType = BitConverter.ToInt32(bytes, 0);
                string moduleTypeDescription = "";
                switch (moduleType)
                {
                    case 0: moduleTypeDescription = "SV Filter"; break;
                    case 1: moduleTypeDescription = "Audio Input"; break;
                    case 2: moduleTypeDescription = "Audio Out"; break;
                    case 3: moduleTypeDescription = "Aliaser"; break;
                    case 4: moduleTypeDescription = "Sequencer"; break;
                    case 5: moduleTypeDescription = "LFO"; break;
                    case 6: moduleTypeDescription = "ADSR"; break;
                    case 7: moduleTypeDescription = "VCA"; break;
                    case 8: moduleTypeDescription = "Audio Multiply"; break;
                    case 9: moduleTypeDescription = "Bit Crusher"; break;
                    case 10: moduleTypeDescription = "Sample and Hold"; break;
                    case 11: moduleTypeDescription = "OD & Distortion"; break;
                    case 12: moduleTypeDescription = "Env Follower"; break;
                    case 13: moduleTypeDescription = "Delay line"; break;
                    case 14: moduleTypeDescription = "Oscillator"; break;
                    case 15: moduleTypeDescription = "Pushbutton"; break;
                    case 16: moduleTypeDescription = "Keyboard"; break;
                    case 17: moduleTypeDescription = "CV Invert"; break;
                    case 18: moduleTypeDescription = "Steps"; break;
                    case 19: moduleTypeDescription = "Slew Limiter"; break;
                    case 20: moduleTypeDescription = "MIDI Notes in"; break;
                    case 21: moduleTypeDescription = "MIDI CC in"; break;
                    case 22: moduleTypeDescription = "Multiplier"; break;
                    case 23: moduleTypeDescription = "Compressor"; break;
                    case 24: moduleTypeDescription = "Multi-filter"; break;
                    case 25: moduleTypeDescription = "Plate Reverb"; break;
                    case 26: moduleTypeDescription = "Buffer delay"; break;
                    case 27: moduleTypeDescription = "All-pass filter"; break;
                    case 28: moduleTypeDescription = "Quantizer"; break;
                    case 29: moduleTypeDescription = "Phaser"; break;
                    case 30: moduleTypeDescription = "Looper"; break;
                    case 31: moduleTypeDescription = "In Switch"; break;
                    case 32: moduleTypeDescription = "Out Switch"; break;
                    case 33: moduleTypeDescription = "Audio In Switch"; break;
                    case 34: moduleTypeDescription = "Audio Out Switch"; break;
                    case 35: moduleTypeDescription = "Midi pressure"; break;
                    case 36: moduleTypeDescription = "Onset Detector"; break;
                    case 37: moduleTypeDescription = "Rhythm"; break;
                    case 38: moduleTypeDescription = "Noise"; break;
                    case 39: moduleTypeDescription = "Random"; break;
                    case 40: moduleTypeDescription = "Gate"; break;
                    case 41: moduleTypeDescription = "Tremolo"; break;
                    case 42: moduleTypeDescription = "Tone Control"; break;
                    case 43: moduleTypeDescription = "Delay w/Mod"; break;
                    case 44: moduleTypeDescription = "Stompswitch"; break;
                    case 45: moduleTypeDescription = "Value"; break;
                    case 46: moduleTypeDescription = "CV Delay"; break;
                    case 47: moduleTypeDescription = "CV Loop"; break;
                    case 48: moduleTypeDescription = "CV Filter"; break;
                    case 49: moduleTypeDescription = "Clock Divider"; break;
                    case 50: moduleTypeDescription = "Comparator"; break;
                    case 51: moduleTypeDescription = "CV Rectify"; break;
                    case 52: moduleTypeDescription = "Trigger"; break;
                    case 53: moduleTypeDescription = "Stereo Spread"; break;
                    case 54: moduleTypeDescription = "Cport Exp/CV in"; break;
                    case 55: moduleTypeDescription = "Cport CV out"; break;
                    case 56: moduleTypeDescription = "UI Button"; break;
                    case 57: moduleTypeDescription = "Audio Panner"; break;
                    case 58: moduleTypeDescription = "Pitch Detector"; break;
                    case 59: moduleTypeDescription = "Pitch Shifter"; break;
                    case 60: moduleTypeDescription = "Midi Note out"; break;
                    case 61: moduleTypeDescription = "Midi CC out"; break;
                    case 62: moduleTypeDescription = "Midi PC out"; break;
                    case 63: moduleTypeDescription = "Bit Modulator"; break;
                    case 64: moduleTypeDescription = "Audio Balance"; break;
                    case 65: moduleTypeDescription = "Inverter"; break;
                    case 66: moduleTypeDescription = "Fuzz"; break;
                    case 67: moduleTypeDescription = "Ghostverb"; break;
                    case 68: moduleTypeDescription = "Cabinet Sim"; break;
                    case 69: moduleTypeDescription = "Flanger"; break;
                    case 70: moduleTypeDescription = "Chorus"; break;
                    case 71: moduleTypeDescription = "Vibrato"; break;
                    case 72: moduleTypeDescription = "Env Filter"; break;
                    case 73: moduleTypeDescription = "Ring Modulator"; break;
                    case 74: moduleTypeDescription = "Hall Reverb"; break;
                    case 75: moduleTypeDescription = "Ping Pong Delay"; break;
                    case 76: moduleTypeDescription = "Audio Mixer"; break;
                    case 77: moduleTypeDescription = "CV Flip Flop"; break;
                    case 78: moduleTypeDescription = "Diffuser"; break;
                    case 79: moduleTypeDescription = "Reverb Lite"; break;
                    case 80: moduleTypeDescription = "Room Reverb"; break;
                    case 81: moduleTypeDescription = "Pixel"; break;
                    case 82: moduleTypeDescription = "Midi Clock In"; break;
                    case 83: moduleTypeDescription = "Granular"; break;
                    default: moduleTypeDescription = "unknown"; break;
                }
                string moduleName = Encoding.UTF8.GetString(bytes, bytes.Length - 16, 16);
                Console.WriteLine(String.Format("Module size = {0}, Module name = {1}", moduleSize, moduleName));
                for (int moduleSection = 0; moduleSection < (moduleSize - 1 - 4); moduleSection++)
                {
                    string description = "unknown";
                    switch (moduleSection)
                    {
                        case 0: description = "Module type";
                            break;
                        case 2: description = "Page number";
                            break;
                        case 3: description = "Old color value";
                            break;
                        case 4: description = "Grid position";
                            break;
                        case 5: description = "Number of parameters on grid"; break;
                        case 7: description = "Module options 1"; break;
                        case 8: description = "Module options 2"; break;
                    }

                    
                
                    int moduleParameterValue = BitConverter.ToInt32(bytes, moduleSection * 4);
                    string moduleParameterValueDescription = "";
                    if (moduleSection == 0)
                    {
                        moduleParameterValueDescription = moduleTypeDescription;
                    }
                    if (moduleSection == 3)
                    {
                        switch(moduleParameterValue)
                        {
                            case 1:
                                moduleParameterValueDescription = "Blue"; break;
                            case 2:
                                moduleParameterValueDescription = "Green"; break;
                            case 3:
                                moduleParameterValueDescription = "Red"; break;
                            case 4:
                                moduleParameterValueDescription = "Yellow"; break;
                            case 5:
                                moduleParameterValueDescription = "Aqua"; break;
                            case 6:
                                moduleParameterValueDescription = "Magenta"; break;
                            case 7:
                                moduleParameterValueDescription = "White"; break;
                        }
                    }
                    if (moduleSection == 7 ||  moduleSection == 8)
                    {
                        moduleParameterValueDescription = String.Format("[{0}, {1}, {2}, {3}]", 
                            bytes[moduleSection * 4 + 0],
                            bytes[moduleSection * 4 + 1],
                            bytes[moduleSection * 4 + 2],
                            bytes[moduleSection * 4 + 3]
                            );
                        
                    }
                    Console.WriteLine(String.Format("{0} ({1}) : {2} ({3})", moduleSection, description, moduleParameterValue, moduleParameterValueDescription));
                }

            }

            bytes = new byte[4];
            fs.Read(bytes, 0, 4);
            int numberOfConnections = BitConverter.ToInt32(bytes, 0);
            Console.WriteLine(String.Format("Number of Connections = {0}", numberOfConnections));

            for (int connectionNumber = 0; connectionNumber < numberOfConnections; connectionNumber++)
            {
                Console.WriteLine(String.Format("Connection #{0}", connectionNumber));
                int connectionSize = 5 * 4;
                bytes = new byte[connectionSize];
                fs.Read(bytes, 0, connectionSize);

                int sourceModule = BitConverter.ToInt32(bytes, 0);
                int sourceOutputNumber = BitConverter.ToInt32(bytes, 4);
                int destinationModule = BitConverter.ToInt32(bytes, 8);
                int destinationInputNumber = BitConverter.ToInt32(bytes, 12);
                int connectionStrength = BitConverter.ToInt32(bytes, 16);
                Console.WriteLine(String.Format("{0}.{1} -> {2}.{3} {4}%", sourceModule, sourceOutputNumber, destinationModule, destinationInputNumber, connectionStrength/100));
            }

            bytes = new byte[4];
            fs.Read(bytes, 0, 4);
            int numberOfPages = BitConverter.ToInt32(bytes, 0);
            Console.WriteLine(String.Format("Number of Pages = {0}", numberOfPages));

            for (int pageNumber = 0; pageNumber < numberOfPages; pageNumber++)
            {
                bytes = new byte[16];
                fs.Read(bytes, 0, 16);
                string pageName = Encoding.UTF8.GetString(bytes, 0, 16);
                Console.WriteLine(String.Format("Page #{0} name = {1}", pageNumber, pageName));
            }
            
            bytes = new byte[4];
            fs.Read(bytes, 0, 4);
            int starredParameterCount = BitConverter.ToInt32(bytes, 0);
            for (int starredParameterNumber = 0; starredParameterNumber < starredParameterCount; starredParameterNumber++)
            {
                bytes = new byte[4];
                fs.Read(bytes, 0, 4);
                int starredParameterValue1 = BitConverter.ToInt16(bytes, 0);
                int starredParameterValue2 = BitConverter.ToInt16(bytes, 2);
                Console.WriteLine("Starred parameter {0} : {1} - {2}", starredParameterNumber, starredParameterValue1, starredParameterValue2);
            }

            for (int moduleColorNumber = 0; moduleColorNumber < numberOfModules; moduleColorNumber++)
            {                
                bytes = new byte[4];
                fs.Read(bytes, 0, 4);
                int moduleColor = BitConverter.ToInt32(bytes, 0);
                string colorDescription = "unknown";
                switch (moduleColor)
                {
                    case 1:
                        colorDescription = "Blue"; break;                    
                    case 2: colorDescription = "Green"; break;
                    case 3: colorDescription = "Red"; break;
                    case 4:
                        colorDescription = "Yellow"; break;
                    case 5:
                        colorDescription = "Aqua"; break;
                    case 6: colorDescription = "Magenta"; break;
                    case 7: colorDescription = "White"; break;
                    case 8: colorDescription = "Orange"; break;
                    case 9: colorDescription = "Lime"; break;
                    case 10: colorDescription = "Surf"; break;
                    case 11: colorDescription = "Sky"; break;
                    case 12: colorDescription = "Purple"; break;
                    case 13: colorDescription = "Pink"; break;
                    case 14: colorDescription = "Peach"; break;
                    case 15: colorDescription = "Mango"; break;
                }
                Console.WriteLine(String.Format("Module #{0} color = {1} ({2})", moduleColorNumber, moduleColor, colorDescription));
            }

            Console.WriteLine(String.Format("Number of bytes read = {0}. Number of blocks = {1}", fs.Position, fs.Position / 4));
            Console.ReadKey();
        }
    }
}
