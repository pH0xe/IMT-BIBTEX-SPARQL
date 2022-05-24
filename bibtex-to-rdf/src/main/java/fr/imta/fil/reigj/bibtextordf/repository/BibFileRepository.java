package fr.imta.fil.reigj.bibtextordf.repository;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

import fr.imta.fil.reigj.bibtextordf.model.BibFile;

@Repository
public interface BibFileRepository extends CrudRepository<BibFile, Long> {
}
