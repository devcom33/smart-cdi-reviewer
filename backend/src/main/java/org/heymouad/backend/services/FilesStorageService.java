package org.heymouad.backend.services;

import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;

public interface FilesStorageService {
    void init();
    void saveFile(MultipartFile file) throws IOException;
}
