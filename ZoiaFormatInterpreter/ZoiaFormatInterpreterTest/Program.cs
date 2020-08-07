using System;
using System.IO;
using System.Text;
using ZoiaFormatInterpreter;

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

            byte[] patchData = new byte[fs.Length];
            fs.Read(patchData, 0, patchData.Length);
            ZoiaPatch zoiaPatch = new ZoiaPatch(patchData);

            Console.WriteLine(String.Format("Preset size = {0}", zoiaPatch.PresetSize));
            Console.WriteLine(String.Format("Patch name = {0}", zoiaPatch.PresetName));
            Console.WriteLine(String.Format("Module count = {0}", zoiaPatch.NumberOfModules));

            foreach (ZoiaModule module in zoiaPatch.ModuleList)
            {                
                Console.WriteLine(String.Format("Module #{0}", zoiaPatch.GetModuleNumber(module)));
                Console.WriteLine(String.Format("Module size = {0}, Module name = {1}, Color = {2} ({3})", module.ModuleSize, module.ModuleUserName, module.ModuleColorId, module.ModuleColorName));
                foreach (ZoiaModuleParameter parameter in module.ParameterList)
                {
                    Console.WriteLine(String.Format("{0} ({1}) : {2} ({3}) - {4}", module.GetParameterNumber(parameter), parameter.ParameterName, parameter.ParameterValue, parameter.ParameterValueDescription, GetLongDescription(parameter.ModuleParameterData)));
                }
            }

            Console.WriteLine(String.Format("Number of Connections = {0}", zoiaPatch.NumberOfConnections));
            foreach (ZoiaConnection connection in zoiaPatch.ConnectionList)
            {
                Console.WriteLine(String.Format("Connection #{0} : {1}.{2} -> {3}.{4} {5}%", 
                    zoiaPatch.ConnectionNumber(connection),
                    connection.SourceModule, 
                    connection.SourceOutputNumber, 
                    connection.DestinationModule, 
                    connection.DestinationInputNumber, 
                    connection.ConnectionStrength / 100));
            }

            Console.WriteLine(String.Format("Number of Pages = {0}", zoiaPatch.NumberOfPages));
            int pageNumber = 0;
            foreach (string pageName in zoiaPatch.PageList)
            {
                Console.WriteLine(String.Format("Page #{0} name = {1}", pageNumber, pageName));
                pageNumber++;
            }

            foreach (ZoiaStarredParameter starredParameter in zoiaPatch.StarredParameterList)
            {                
                Console.WriteLine("Starred parameter {0} : {1}", zoiaPatch.GetStarredParameterNumber(starredParameter), GetLongDescription(starredParameter.StarredParameterData));
            }
            
            Console.WriteLine(String.Format("Number of bytes read = {0}. Number of blocks = {1}", zoiaPatch.NumberOfBytesParsed, zoiaPatch.NumberOfBytesParsed / 4));
        }        

        public static string GetLongDescription(byte[] bytes)
        {
            string longDescription =
                 String.Format("0x{0} = [{1}, {2}, {3}, {4}] = [{5}, {6}]",
                    BitConverter.ToString(bytes),   
                    bytes[0],
                    bytes[1],
                    bytes[2],
                    bytes[3],
                    BitConverter.ToInt16(bytes, 0),
                    BitConverter.ToInt16(bytes, 2)
                    );

            return longDescription;            
        }
    }
}
