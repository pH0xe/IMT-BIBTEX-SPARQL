package fr.imta.fil.reigj.bibtextordf.model;

import java.util.Objects;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Lob;
import javax.persistence.Table;

import com.fasterxml.jackson.annotation.JsonIgnore;

@Entity
@Table(name = "bibfile")
public class BibFile {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private long id;
    @Column(name = "uploaddate")
    private long uploadDate;
    private String name;

    @JsonIgnore
    @Lob
    private byte[] data;
    private long size;
    @Column(name = "contenttype")
    private String contentType;

    public BibFile() {
    }

    public long getSize() {
        return size;
    }

    public void setSize(long size) {
        this.size = size;
    }

    public BibFile(byte[] data, String name, long uploadDate) {
        this.data = data;
        this.name = name;
        this.uploadDate = uploadDate;
    }

    public long getId() {
        return id;
    }

    public void setId(long id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public long getUploadDate() {
        return uploadDate;
    }

    public void setUploadDate(long uploadDate) {
        this.uploadDate = uploadDate;
    }

    public byte[] getData() {
        return data;
    }

    public void setData(byte[] data) {
        this.data = data;
    }

    public String getContentType() {
        return contentType;
    }

    public void setContentType(String contentType) {
        this.contentType = contentType;
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) {
            return true;
        }
        if (obj == null) {
            return false;
        }
        if (getClass() != obj.getClass()) {
            return false;
        }
        final BibFile other = (BibFile) obj;

        return Objects.equals(this.id, other.id);
    }

    @Override
    public String toString() {
        return "BibFile : { id: (" + this.id + "), name: (" + this.name + "), uploadDate: (" + this.uploadDate + ")}";
    }
}
