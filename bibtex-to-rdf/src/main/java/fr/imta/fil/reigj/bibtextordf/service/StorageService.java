package fr.imta.fil.reigj.bibtextordf.service;

import fr.imta.fil.reigj.bibtextordf.model.BibFile;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;

public interface StorageService {
    List<BibFile> loadAll();
    BibFile getOne(int id);
    void uploadOne(MultipartFile file);
}
