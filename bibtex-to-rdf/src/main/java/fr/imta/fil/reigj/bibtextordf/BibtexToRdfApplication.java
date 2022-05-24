package fr.imta.fil.reigj.bibtextordf;

import fr.imta.fil.reigj.bibtextordf.config.FileUploadConfiguration;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.EnableConfigurationProperties;

@SpringBootApplication
@EnableConfigurationProperties({
        FileUploadConfiguration.class
})
public class BibtexToRdfApplication {
    public static void main(String[] args) {
        SpringApplication.run(BibtexToRdfApplication.class, args);
    }

}
