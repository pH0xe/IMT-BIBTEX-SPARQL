package fr.imta.fil.reigj.bibtextordf.service;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

@Service
public class ConverterService {

    private final String pathStr = "dataFiles";
    private final Path path = Paths.get(pathStr);
    private boolean isInit = false;

    public ConverterService() {
        if (!Files.exists(path)) {
            try {
                Files.createDirectory(path);
            } catch (IOException e) {
                throw new RuntimeException("Could not initialize folder for upload!");
            }
        }
        isInit = true;
    }

    public void init() {

    }

    public Path saveOnDisk(MultipartFile file) throws IOException {
        Path tempFile = Files.createTempFile(null, ".lib");

        try {
            Files.write(tempFile, file.getBytes());
        } catch (Exception e) {
            throw new RuntimeException("Could not store the file. Error: " + e.getMessage());
        }

        return tempFile;
    }

    public void convertToRDF(MultipartFile file) throws IOException {
        if (!isInit)
            return;
        if (file == null) {
            // TODO: restore a partir de la bd
            throw new UnsupportedOperationException("Methode not implemented, restore from Database");
        }
        Path bibFile = saveOnDisk(file);

        ProcessBuilder processBuilder = new ProcessBuilder("java", "-jar",
                "bibtex2rdf.jar", "-enc", "UTF-8", bibFile.toString(),
                pathStr + "/bib.rdf");

        System.out.println("Start process");
        Process process = processBuilder.start();
        try {
            System.out.println("waiting for :");
            int exitCode = process.waitFor();
            System.out.println(exitCode);
        } catch (InterruptedException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }

    }
}
