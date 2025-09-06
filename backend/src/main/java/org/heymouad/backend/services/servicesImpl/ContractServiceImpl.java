package org.heymouad.backend.services.servicesImpl;

import lombok.RequiredArgsConstructor;
import org.apache.tika.exception.TikaException;
import org.heymouad.backend.dtos.ContractResponse;
import org.heymouad.backend.services.ClauseExtractionService;
import org.heymouad.backend.services.ClauseProcessingService;
import org.heymouad.backend.services.ContractService;
import org.heymouad.backend.services.FilesStorageService;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;
import org.xml.sax.SAXException;

import java.io.IOException;
import java.nio.file.Path;
import java.util.List;


@Service
@RequiredArgsConstructor
public class ContractServiceImpl implements ContractService {
    private final ClauseExtractionService clauseExtractionService;
    private final ClauseProcessingService clauseProcessingService;
    private final FilesStorageService filesStorageService;


    @Override
    public ContractResponse processContract(MultipartFile file) throws IOException, TikaException, SAXException {
        // save file
        String storedFileName = filesStorageService.saveFile(file);
        Path filePath = Path.of("/var/data/uploads").resolve(storedFileName);

        // extract text
        String extractedText = clauseExtractionService.extractText(filePath);

        // extract clauses
        List<String> clauses = clauseProcessingService.splitIntoClauses(extractedText);

        return new ContractResponse(storedFileName, extractedText, clauses);
    }
}
