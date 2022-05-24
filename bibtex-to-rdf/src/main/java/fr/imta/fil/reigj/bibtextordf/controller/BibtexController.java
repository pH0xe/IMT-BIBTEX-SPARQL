package fr.imta.fil.reigj.bibtextordf.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("api")
public class BibtexController {

    @PostMapping("/bibtex")
    public ResponseEntity<String> uploadBibtex(@RequestParam(value="file", required = false) MultipartFile file) {
        if (file == null) {
            return ResponseEntity.badRequest().body("no file provided");
        }
        if (file.isEmpty()) {
            return ResponseEntity.badRequest().body("File is empty");
        }

        return ResponseEntity.ok().body("Everythings good");
    }
}
