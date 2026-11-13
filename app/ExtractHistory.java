import net.jpountz.lz4.LZ4Factory;
import net.jpountz.lz4.LZ4FastDecompressor;
import java.io.*;
import java.nio.file.Files;
import java.util.ArrayList;

public class ExtractHistory {
    public static void main(String[] args) throws Exception {
        byte[] data = Files.readAllBytes(new File("/Users/piergaetanopalella/Library/Caches/Google/AndroidStudio2026.1.4/LocalHistory/changes.storageData").toPath());
        LZ4Factory factory = LZ4Factory.fastestInstance();
        LZ4FastDecompressor decompressor = factory.fastDecompressor();
        
        System.out.println("Data size: " + data.length);
        
        // This is a naive extraction. IntelliJ LocalHistory format is more complex.
        // It's a sequence of records. Let's just try to find "package it.fm.spese" in blocks.
        // Since we don't know the exact blocks, maybe we can search for the frame magic or block sizes.
    }
}
