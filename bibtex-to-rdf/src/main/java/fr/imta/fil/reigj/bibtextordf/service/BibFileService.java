package fr.imta.fil.reigj.bibtextordf.service;

import java.io.IOException;
import java.util.List;

import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;
import org.springframework.web.multipart.MultipartFile;

import fr.imta.fil.reigj.bibtextordf.model.BibFile;
import fr.imta.fil.reigj.bibtextordf.repository.BibFileRepository;

@Service
public class BibFileService implements IBibFileService {

    private final BibFileRepository bibFileRepository;

    public BibFileService(BibFileRepository bibFileRepository) {
        this.bibFileRepository = bibFileRepository;
    }

    @Override
    public List<BibFile> findAll() {
        return (List<BibFile>) this.bibFileRepository.findAll();
    }

    @Override
    public BibFile save(MultipartFile file) throws IOException {
        BibFile bFile = new BibFile();
        bFile.setUploadDate(System.currentTimeMillis());
        bFile.setName(StringUtils.cleanPath(file.getOriginalFilename()));
        bFile.setData(file.getBytes());
        bFile.setContentType(file.getContentType());
        bFile.setSize(file.getSize());
        return this.bibFileRepository.save(bFile);
    }

    @Override
    public void remove(long id) {
        this.bibFileRepository.deleteById(id);
    }

}
