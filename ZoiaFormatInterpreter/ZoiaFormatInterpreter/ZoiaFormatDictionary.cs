using System;
using System.Collections.Generic;
using System.Text;
using Newtonsoft.Json;
using Microsoft.CSharp.RuntimeBinder;
using System.Runtime.Serialization;

namespace ZoiaFormatInterpreter
{
    public class ZoiaFormatDictionary
    {
        protected ZoiaDictionary zoiaDictionary;

        public ZoiaFormatDictionary(string json)
        {
            dynamic data = JsonConvert.DeserializeObject(json, typeof(ZoiaDictionary));
            zoiaDictionary = data;
        }

        public ZoiaDictionaryModule findModuleByTypeId(int typeId)
        {
            return zoiaDictionary.modules[typeId];
        }

        public string getModuleName(int typeId)
        {
            return findModuleByTypeId(typeId).name;
        }
    }

    public class ZoiaDictionary
    {
        public List<ZoiaDictionaryModule> modules { get; set; }
    }

    [DataContract]
    public class ZoiaDictionaryModule
    {
        [DataMember]
        public string name { get; set; }
        /*[DataMember]
        public string category { get; set; }
        [DataMember]
        public int max_blocks { get; set; }
        [DataMember(Name = "params")]
        public int Params { get; set; }
        [DataMember]
        public List<object> blocks { get; set; }*/
        [DataMember]
        public List<ZoiaDictionaryOption> options { get; set; }
    }

    public class ZoiaDictionaryOption
    {
        public string name { get; set; }
        public List<string> values { get; set; }
    }


}
