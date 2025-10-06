package org.heymouad.backend.services;

import java.util.List;

public interface ClauseProcessingService {
    List<String> splitIntoClauses(String text);
}
