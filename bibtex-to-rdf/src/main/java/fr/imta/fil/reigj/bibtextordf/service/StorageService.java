package fr.imta.fil.reigj.bibtextordf.service;

import fr.imta.fil.reigj.bibtextordf.model.BibFile;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;

@Service
public class StorageService implements IStorageService{
    @Override
    public List<BibFile> loadAll() {
        return null;
    }

    @Override
    public BibFile getOne(int id) {
        return null;
    }

    @Override
    public BibFile uploadOne(MultipartFile file) {
        return null;
    }

    @Override
    public void delete(int id) {

    }
}
