package org.heymouad.backend.services.servicesImpl;

import org.apache.tika.exception.TikaException;
import org.apache.tika.metadata.Metadata;
import org.apache.tika.parser.AutoDetectParser;
import org.apache.tika.parser.ParseContext;
import org.apache.tika.sax.BodyContentHandler;
import org.heymouad.backend.services.ClauseExtractionService;
import org.springframework.stereotype.Service;
import org.xml.sax.SAXException;

import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;

@Service
public class ClauseExtractionServiceImpl implements ClauseExtractionService {
    @Override
    public String extractText(Path filePath) throws IOException, TikaException, SAXException {
        AutoDetectParser parser = new AutoDetectParser();
        BodyContentHandler handler = new BodyContentHandler(-1);
        Metadata metadata = new Metadata();

        try (InputStream stream = Files.newInputStream(filePath))
        {
            parser.parse(stream, handler, metadata, new ParseContext());
        }

        return handler.toString();
    }
}
