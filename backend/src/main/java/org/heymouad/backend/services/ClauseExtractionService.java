package org.heymouad.backend.services;

import org.apache.tika.exception.TikaException;
import org.xml.sax.SAXException;

import java.io.IOException;
import java.nio.file.Path;

public interface ClauseExtractionService {
    String extractText(Path filePath) throws IOException, TikaException, SAXException;
}
