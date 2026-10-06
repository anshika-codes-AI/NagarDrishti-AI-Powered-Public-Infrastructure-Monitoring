from .activities.analyze_image import AnalyzeImageActivity
from .activities.analyze_video import AnalyzeVideoActivity


class Dispatcher:
    """Simple synchronous dispatcher that routes media to the correct activity."""

    @staticmethod
    def dispatch(media_type: str, file_path: str, location=None):
        """Route media to the appropriate activity.

        Args:
            media_type: "image" or "video"
            file_path: path to the uploaded media file
            location: optional dict with latitude/longitude/location_name

        Returns:
            dict with "analysis" and "report" keys
        """
        if media_type == "image":
            activity = AnalyzeImageActivity()
            return activity.run(file_path, location)
        elif media_type == "video":
            activity = AnalyzeVideoActivity()
            return activity.run(file_path, location)
        else:
            raise ValueError(f"Unsupported media type: {media_type}")