package fr.imta.fil.reigj.bibtextordf.service;

import fr.imta.fil.reigj.bibtextordf.model.BibFile;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;

public interface IStorageService {
    List<BibFile> loadAll();
    BibFile getOne(int id);
    BibFile uploadOne(MultipartFile file);
    void delete(int id);
}
