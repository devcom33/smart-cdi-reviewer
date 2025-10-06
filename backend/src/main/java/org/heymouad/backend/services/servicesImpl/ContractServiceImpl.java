package org.heymouad.backend.services.servicesImpl;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.tika.exception.TikaException;
import org.heymouad.backend.dtos.ClauseResponse;
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
import java.util.ArrayList;
import java.util.List;
import java.util.stream.IntStream;


@Service
@RequiredArgsConstructor
@Slf4j
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

        // cleaning
        String cleanedText = extractedText.replaceAll("\\s{2,}", "\n");
        cleanedText = cleanedText.replaceAll("\n", " ");
        // extract clauses
        List<String> splitText = new ArrayList<>(clauseProcessingService.splitIntoClauses(cleanedText));
        String header = null;
        List<ClauseResponse> clauses = List.of();

        if (!splitText.isEmpty()) {
            header = splitText.get(0);
            clauses = IntStream.range(0, splitText.size() - 1)
                    .mapToObj(i -> new ClauseResponse(i + 1, splitText.get(i + 1)))
                    .toList();
        }

        return new ContractResponse(storedFileName, extractedText, header, clauses);
    }
}
