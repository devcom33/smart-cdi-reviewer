package org.heymouad.backend.services;

import org.springframework.core.io.Resource;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;

public interface FilesStorageService {
    void init();
    String saveFile(MultipartFile file) throws IOException;
    Resource loadAsResouce(String filename);
}
