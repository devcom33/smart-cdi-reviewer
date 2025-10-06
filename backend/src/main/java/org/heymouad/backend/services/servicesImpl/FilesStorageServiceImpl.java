package org.heymouad.backend.services.servicesImpl;

import org.heymouad.backend.services.FilesStorageService;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.Resource;
import org.springframework.core.io.UrlResource;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.io.InputStream;
import java.net.MalformedURLException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.Objects;
import java.util.UUID;


@Service
public class FilesStorageServiceImpl implements FilesStorageService {
    private final Path rootLocation;

    public FilesStorageServiceImpl(@Value("${app.upload-dir}") String uploadDir)
    {
        this.rootLocation = Paths.get(uploadDir).toAbsolutePath().normalize();
        init();
    }
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
    public String saveFile(MultipartFile file) throws IOException {
        if (file.isEmpty()) throw new IllegalArgumentException("Empty file");

        init();

        String original = StringUtils.cleanPath(Objects.requireNonNull(file.getOriginalFilename()));
        if (original.contains("..")) throw new IllegalArgumentException("Invalid Path");

        String stored = UUID.randomUUID() + "-" + original;

        try (InputStream inputStream = file.getInputStream()) {
            Files.copy(inputStream, this.rootLocation.resolve(stored), StandardCopyOption.REPLACE_EXISTING);
        }

        return stored;
    }

    @Override
    public Resource loadAsResouce(String filename) {
        try{
            Path file = this.rootLocation.resolve(filename).normalize();
            Resource resource = new UrlResource(file.toUri());
            if (!resource.exists() || !resource.isReadable()) throw new IllegalArgumentException("Not Found");
            return resource;
        } catch (MalformedURLException e) {
            throw new IllegalArgumentException("Bad filename", e);
        }
    }
}
