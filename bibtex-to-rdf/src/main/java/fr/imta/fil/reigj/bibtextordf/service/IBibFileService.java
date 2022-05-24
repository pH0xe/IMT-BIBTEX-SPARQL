package fr.imta.fil.reigj.bibtextordf.service;

import java.io.IOException;
import java.util.List;

import org.springframework.web.multipart.MultipartFile;

import fr.imta.fil.reigj.bibtextordf.model.BibFile;

public interface IBibFileService {
    List<BibFile> findAll();

    BibFile save(MultipartFile file) throws IOException;

    void remove(long id);
}
