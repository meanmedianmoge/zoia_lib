using System;
using System.Collections.Generic;
using System.Text;

namespace ZoiaFormatInterpreter
{
    public class ZoiaPatch
    {
        public ZoiaFormatDictionary FormatDictionary { get; set; }
        public byte[] PatchData { get; protected set; }
        public int PresetSize { get; set; }
        public string PresetName { get; set; }

        public int NumberOfModules { get
            {
                return ModuleList.Count;
            }
        }

        protected List<ZoiaModule> _moduleList;
        public List<ZoiaModule> ModuleList
        {
            get {
                if (_moduleList == null)
                {
                    _moduleList = new List<ZoiaModule>();
                }
                return _moduleList;
            }
            protected set { _moduleList = value; }
        }

        protected List<ZoiaConnection> _connectionList;
        public List<ZoiaConnection> ConnectionList {
            get
            {
                if (_connectionList == null) {
                    _connectionList = new List<ZoiaConnection>();
                } return _connectionList;
            }
            protected set
            {
                _connectionList = value;
            }
        }
        public int NumberOfConnections { get {
                return ConnectionList.Count;
            }
        }

        protected List<string> _pageList;

        public List<string> PageList { get
            {
                if (_pageList == null)
                {
                    _pageList = new List<string>();
                }
                return _pageList;
            }
            protected set
            {
                _pageList = value;
            }
        }
        public int NumberOfPages { get { return PageList.Count; } }

        protected List<ZoiaStarredParameter> _starredParameterList;
        public List<ZoiaStarredParameter> StarredParameterList {
            get {
                if (_starredParameterList == null)
                {
                    _starredParameterList = new List<ZoiaStarredParameter>();
                }
                return _starredParameterList;
            }
            protected set { _starredParameterList = value; } }

        public int NumberOfBytesParsed { get; protected set; }

        public ZoiaPatch(byte[] patchData, ZoiaFormatDictionary zoiaFormatDictionary) 
        {
            PatchData = patchData;
            FormatDictionary = zoiaFormatDictionary;
            ParseData();
        }        

        public void ParseData()
        {
            int dataSizeUnit = 4;
            PresetSize = BitConverter.ToInt32(PatchData, 0);
            PresetName = Encoding.UTF8.GetString(PatchData, 4, 16);
            int numberOfModules = BitConverter.ToInt32(PatchData, 20);

            int dataPosition = 24;
            for (int moduleNumber = 0; moduleNumber < numberOfModules; moduleNumber++)
            {                
                int moduleSize = BitConverter.ToInt32(PatchData, dataPosition) * dataSizeUnit;                
                byte[] moduleData = new byte[moduleSize];
                Array.Copy(PatchData, dataPosition, moduleData, 0, moduleSize);
                ModuleList.Add(new ZoiaModule(moduleData, FormatDictionary));
                dataPosition += moduleSize;
            }
                        
            int numberOfConnections = BitConverter.ToInt32(PatchData, dataPosition);
            dataPosition += dataSizeUnit;
            int connectionSize = 20;
            for (int connectionNumber = 0; connectionNumber < numberOfConnections; connectionNumber++)
            {                                
                byte[] connectionData = new byte[connectionSize];
                Array.Copy(PatchData, dataPosition, connectionData, 0, connectionSize);
                this.ConnectionList.Add(new ZoiaConnection(connectionData));
                dataPosition += connectionSize;
            }
            
            int numberOfPages = BitConverter.ToInt32(PatchData, dataPosition);
            dataPosition += dataSizeUnit;
            int pageSize = 16;
            for (int pageNumber = 0; pageNumber < numberOfPages; pageNumber++)
            {                                
                string pageName = Encoding.UTF8.GetString(PatchData, dataPosition, pageSize);
                PageList.Add(pageName);
                dataPosition += pageSize;                
            }
            
            int starredParameterCount = BitConverter.ToInt32(PatchData, dataPosition);
            dataPosition += dataSizeUnit;
            int starredParameterSize = 4;
            for (int starredParameterNumber = 0; starredParameterNumber < starredParameterCount; starredParameterNumber++)
            {
                byte[] starredParameterData = new byte[starredParameterSize];
                Array.Copy(PatchData, dataPosition, starredParameterData, 0, starredParameterSize);
                StarredParameterList.Add(new ZoiaStarredParameter(starredParameterData));
                dataPosition += starredParameterSize;
            }

            int moduleColorSize = 4;            
            for (int moduleColorNumber = 0; moduleColorNumber < numberOfModules; moduleColorNumber++)
            {                
                int moduleColor = BitConverter.ToInt32(PatchData, dataPosition);
                ModuleList[moduleColorNumber].ModuleColorId = moduleColor;
                
                dataPosition += moduleColorSize;                
            }
            NumberOfBytesParsed = dataPosition;
        }

        public int GetStarredParameterNumber(ZoiaStarredParameter starredParameter)
        {
            return StarredParameterList.IndexOf(starredParameter);
        }

        public int GetPageNumber(string pageName)
        {
            return PageList.IndexOf(pageName);
        }

        public int ConnectionNumber(ZoiaConnection connection)
        {
            return this.ConnectionList.IndexOf(connection);
        }

        public int GetModuleNumber(ZoiaModule zoiaModule)
        {
            return ModuleList.IndexOf(zoiaModule);
        }
    }

    public class ZoiaStarredParameter
    {
        public byte[] StarredParameterData { get; protected set; }

        public ZoiaStarredParameter(byte[] starredParameterData)
        {
            this.StarredParameterData = starredParameterData;
        }
    }

    public class ZoiaConnection
    {
        public byte[] ConnectionData { get; protected set; }
        public int SourceModule { get; protected set; }
        public int SourceOutputNumber { get; protected set; }
        public int DestinationModule { get; protected set; }
        public int DestinationInputNumber { get; protected set; }
        public int ConnectionStrength { get; protected set; }

        public ZoiaConnection(byte[] connectionData)
        {
            this.ConnectionData = connectionData;
            ParseData();
        }

        public void ParseData()
        {
            SourceModule = BitConverter.ToInt32(ConnectionData, 0);
            SourceOutputNumber = BitConverter.ToInt32(ConnectionData, 4);
            DestinationModule = BitConverter.ToInt32(ConnectionData, 8);
            DestinationInputNumber = BitConverter.ToInt32(ConnectionData, 12);
            ConnectionStrength = BitConverter.ToInt32(ConnectionData, 16);
        }
    }

    public class ZoiaModule
    {

        public ZoiaFormatDictionary FormatDictionary {get; set;}
        public byte[] ModuleData { get; protected set; }
        public int ModuleTypeId { get; set; }
        public int ModuleSize { get; protected set; }
        public string
        {
            get
            {
                return Get(ModuleTypeId);
            }
        }

        protected List<ZoiaModuleParameter> _parameterList;
        public List<ZoiaModuleParameter> ParameterList
        {
            get
            {
                if (_parameterList == null)
                {
                    _parameterList = new List<ZoiaModuleParameter>();
                }
                return _parameterList;
            }
            protected set { _parameterList = value; }
        }

        public string ModuleUserName { get; set; }
        public int ModuleColorId { get; set; }

        public string ModuleColorName
        {
            get { return GetColorName(ModuleColorId); }
        }

        public ZoiaModule(byte[] moduleData, ZoiaFormatDictionary formatDictionary)
        {
            ModuleData = moduleData;
            FormatDictionary = formatDictionary;
            ParseData();
        }

        public string Get(int moduleTypeId)
        {
            return FormatDictionary.getModuleName(moduleTypeId);            
        }

        public void ParseData()
        {
            ModuleSize = BitConverter.ToInt32(ModuleData, 0);
            ModuleTypeId = BitConverter.ToInt32(ModuleData, 4);
            ZoiaDictionaryModule dictionaryModule = FormatDictionary.findModuleByTypeId(ModuleTypeId);
            ModuleUserName = Encoding.UTF8.GetString(ModuleData, ModuleData.Length - 16, 16);
            
            for (int moduleSection = 0; moduleSection < 9; moduleSection++)
            {                
                string parameterName = GetParameterName(moduleSection);

                int moduleParameterValue = BitConverter.ToInt32(ModuleData, (moduleSection + 1) * 4);
                string moduleParameterValueDescription = "";
                if (moduleSection == 0)
                {
                    moduleParameterValueDescription = ;
                }
                if (moduleSection == 3)
                {
                    moduleParameterValueDescription = GetColorName(moduleParameterValue);
                }                                 
                
                int parameterSize = 4;
                byte[] parameterData = new byte[parameterSize];
                Array.Copy(ModuleData, (moduleSection + 1) * 4, parameterData, 0, parameterSize);
                ZoiaModuleParameter parameter = new ZoiaModuleParameter(parameterData) {
                    ParameterName = parameterName,
                    ParameterValue = moduleParameterValue,
                    ParameterValueDescription = moduleParameterValueDescription
                };
                ParameterList.Add(parameter);
            }
            for (int i = 0; i < dictionaryModule.options.Count; i++)
            {
                byte[] parameterData = new byte[1];
                Array.Copy(ModuleData, 8 * 4 + i, parameterData, 0, 1);
                ZoiaDictionaryOption dictionaryOption = dictionaryModule.options[i];
                string parameterName = dictionaryOption.name;
                int moduleParameterValue = parameterData[0];
                string moduleParameterValueDescription = dictionaryOption.values[moduleParameterValue];
                ZoiaModuleParameter parameter = new ZoiaModuleParameter(parameterData)
                {
                    ParameterName = parameterName,
                    ParameterValue = moduleParameterValue,
                    ParameterValueDescription = moduleParameterValueDescription
                };
                ParameterList.Add(parameter);
            }
            int numberOfParameterBlocks = ModuleSize - 5; // excluding ModuleSize(1), ModuleUserName(4)
        }

        public string GetParameterName(int moduleSection)
        {
            string description = "unknown";
            switch (moduleSection)
            {
                case 0:
                    description = "Module type";
                    break;
                case 2:
                    description = "Page number";
                    break;
                case 3:
                    description = "Old color value";
                    break;
                case 4:
                    description = "Grid position";
                    break;
                case 5: description = "Number of parameters on grid"; break;
                case 7: description = "Module options 1"; break;
                case 8: description = "Module options 2"; break;
            }

            return description;
        }

        public string GetColorName(int moduleColorId)
        {
            string colorDescription = "unknown";
            switch (moduleColorId)
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

            return colorDescription;
        }

        public int GetParameterNumber(ZoiaModuleParameter parameter)
        {
            return ParameterList.IndexOf(parameter);
        }
    }

    public class ZoiaModuleParameter
    {
        public byte[] ModuleParameterData { get; protected set; }

        public string ParameterName { get; set; }
        public int ParameterValue { get; set; }
        public string ParameterValueDescription { get; set; }

        public ZoiaModuleParameter(byte[] moduleParameterData)
        {
            ModuleParameterData = moduleParameterData;            
        }        

    }
}
