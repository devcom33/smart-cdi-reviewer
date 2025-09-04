package org.heymouad.backend.services.servicesImpl;

import org.heymouad.backend.services.FilesStorageService;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.Objects;



@Service
public class FilesStorageServiceImpl implements FilesStorageService {
    private final Path rootLocation = Paths.get("uploads");


    @Override
    public void init() {
        try {
            if (!Files.exists(rootLocation)) {
                Files.createDirectories(rootLocation);
            }
        } catch (Exception e) {
            throw new RuntimeException("Error : Could not initialize folder for upload!");
        }
    }

    @Override
    public void saveFile(MultipartFile file) throws IOException {
        init();
        try (InputStream inputStream = file.getInputStream()) {
            Path filePath = this.rootLocation.resolve(Objects.requireNonNull(file.getOriginalFilename()));
            Files.copy(inputStream, filePath, StandardCopyOption.REPLACE_EXISTING);
        } catch (Exception e)
        {
            throw new IOException(e.getMessage());
        }
    }
}
