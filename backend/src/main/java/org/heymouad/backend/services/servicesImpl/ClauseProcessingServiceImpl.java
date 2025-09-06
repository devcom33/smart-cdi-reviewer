package org.heymouad.backend.services.servicesImpl;

import org.heymouad.backend.services.ClauseProcessingService;
import org.springframework.stereotype.Service;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Stream;

@Service
public class ClauseProcessingServiceImpl implements ClauseProcessingService {
    @Override
    public List<String> splitIntoClauses(String text) {
        return Arrays.stream(text.split("(?=Article\\\\s+[IVXLC0-9]+)"))
                .map(String::trim)
                .filter(s -> !s.isBlank())
                .toList();
    }
}
