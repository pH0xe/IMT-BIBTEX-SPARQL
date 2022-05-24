package fr.imta.fil.reigj.bibtextordf.controller;

import fr.imta.fil.reigj.bibtextordf.model.BibFile;
import fr.imta.fil.reigj.bibtextordf.service.BibFileService;
import fr.imta.fil.reigj.bibtextordf.service.ConverterService;

import java.io.IOException;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("api")
public class BibtexController {

    private final BibFileService bibFileService;
    private final ConverterService converterService;

    public BibtexController(BibFileService bibFileService, ConverterService converterService) {
        this.bibFileService = bibFileService;
        this.converterService = converterService;
    }

    @PostMapping("/bibtex")
    public ResponseEntity<?> uploadBibtex(@RequestParam(value = "file", required = false) MultipartFile file)
            throws IOException {
        if (file == null) {
            return ResponseEntity.badRequest().body("no file provided");
        }
        if (file.isEmpty()) {
            return ResponseEntity.badRequest().body("File is empty");
        }

        converterService.convertToRDF(file);
        // BibFile newFile = this.bibFileService.save(file);
        BibFile newFile = new BibFile();
        if (newFile == null) {
            return ResponseEntity.internalServerError().body("Unable to upload File");
        }
        return ResponseEntity.ok().body(newFile);
    }

    @GetMapping("/bibtex")
    public ResponseEntity<?> getAll() {
        return ResponseEntity.ok(bibFileService.findAll());
    }

    @DeleteMapping("/bibtex/{id}")
    public ResponseEntity<?> removeById(@PathVariable long id) {
        bibFileService.remove(id);
        return ResponseEntity.ok().build();
    }

    // @GetMapping("/download/{fileName}")
    // public ResponseEntity<Resource> downloadFile(@PathVariable String fileName) {
    // FileModel model = fileService.getFile(fileName);
    // return ResponseEntity.ok().
    // header(HttpHeaders.CONTENT_DISPOSITION, "attachment;filename=\"" +
    // model.getFileName() + "\"").
    // body(new ByteArrayResource(model.getFileData())); // byte[]

    // }
}
