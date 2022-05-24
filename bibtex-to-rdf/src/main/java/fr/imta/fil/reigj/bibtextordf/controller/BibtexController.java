package fr.imta.fil.reigj.bibtextordf.controller;

import fr.imta.fil.reigj.bibtextordf.model.BibFile;
import fr.imta.fil.reigj.bibtextordf.service.StorageService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("api")
public class BibtexController {

    private final StorageService storageService;

    public BibtexController(StorageService storageService) {
        this.storageService = storageService;
    }

    @PostMapping("/bibtex")
    public ResponseEntity<?> uploadBibtex(@RequestParam(value="file", required = false) MultipartFile file) {
        if (file == null) {
            return ResponseEntity.badRequest().body("no file provided");
        }
        if (file.isEmpty()) {
            return ResponseEntity.badRequest().body("File is empty");
        }
        BibFile newFile = this.storageService.uploadOne(file);
        if (newFile == null) {
            return ResponseEntity.internalServerError().body("Unable to upload File");
        }
        return ResponseEntity.ok().body(newFile);
    }
}
